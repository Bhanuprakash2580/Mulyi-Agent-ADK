import os
import logging
import google.cloud.logging
import sys

sys.path.append("..")
from callback_logging import log_query_to_model, log_model_response
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool
from google.adk.models import Gemini
from google.genai import types

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from adk_utils.plugins import Graceful429Plugin
from google.adk.apps.app import App

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from google.adk.tools import exit_loop

# Logging setup
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()

model_name = os.getenv("MODEL")
RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=1, attempts=6)

# =========================
# TOOLS
# =========================

def append_to_state(tool_context: ToolContext, field: str, response: str):
    existing_state = tool_context.state.get(field, [])
    tool_context.state[field] = existing_state + [response]
    logging.info(f"[Added to {field}] {response}")
    return {"status": "success"}


def write_file(tool_context: ToolContext, directory: str, filename: str, content: str):
    target_path = os.path.join(directory, filename)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w") as f:
        f.write(content)
    return {"status": "success"}


# =========================
# AGENTS
# =========================

critic = Agent(
    name="critic",
    model=Gemini(model=model_name, retry_options=RETRY_OPTIONS),
    description="Reviews and improves the plot outline.",
    instruction="""
    INSTRUCTIONS:
    Carefully review the PLOT_OUTLINE.

    - Check story structure (beginning, middle, end)
    - Check character engagement
    - Check historical accuracy

    ALWAYS provide a clear response explaining your analysis.

    If the PLOT_OUTLINE is strong and complete:
    → Call 'exit_loop'
    → Clearly explain why it is ready

    If improvements are needed:
    → Use 'append_to_state' to add feedback into 'CRITICAL_FEEDBACK'
    → Explain what needs improvement

    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    RESEARCH:
    { research? }
    """,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[append_to_state, exit_loop],
)

screenwriter = Agent(
    name="screenwriter",
    model=Gemini(model=model_name, retry_options=RETRY_OPTIONS),
    description="Writes and improves plot outline.",
    instruction="""
    INSTRUCTIONS:
    Write a logline and three-act plot outline.

    - Use PROMPT as base idea
    - Improve using CRITICAL_FEEDBACK if available
    - Use RESEARCH for realism
    - Improve existing PLOT_OUTLINE if present

    Use 'append_to_state' to store result in 'PLOT_OUTLINE'

    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    RESEARCH:
    { research? }

    CRITICAL_FEEDBACK:
    { CRITICAL_FEEDBACK? }

    PROMPT:
    { PROMPT? }
    """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[append_to_state],
)

researcher = Agent(
    name="researcher",
    model=Gemini(model=model_name, retry_options=RETRY_OPTIONS),
    description="Researches using Wikipedia.",
    instruction="""
    PROMPT:
    { PROMPT? }

    INSTRUCTIONS:
    - Use Wikipedia tool for research
    - Improve based on CRITICAL_FEEDBACK if available
    - Add realism to PLOT_OUTLINE

    Store research using 'append_to_state' in 'research'
    """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[
        LangchainTool(tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())),
        append_to_state,
    ],
)

file_writer = Agent(
    name="file_writer",
    model=Gemini(model=model_name, retry_options=RETRY_OPTIONS),
    description="Writes final output to file.",
    instruction="""
    INSTRUCTIONS:
- Create a marketable, contemporary movie title suggestion for the movie described in the PLOT_OUTLINE. If a title has been suggested in PLOT_OUTLINE, you can use it, or replace it with a better one.
- Use your 'write_file' tool to create a new txt file with the following arguments:
    - for a filename, use the movie title
    - Write to the 'movie_pitches' directory.
    - For the 'content' to write, include:
        - The PLOT_OUTLINE
        - The BOX_OFFICE_REPORT
        - The CASTING_REPORT

PLOT_OUTLINE:
{ PLOT_OUTLINE? }

BOX_OFFICE_REPORT:
{ box_office_report? }

CASTING_REPORT:
{ casting_report? }
    """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[write_file],
)

# =========================
# WORKFLOW AGENTS
# =========================

writers_room = LoopAgent(
    name="writers_room",
    description="Iteratively improves the story",
    sub_agents=[
        researcher,
        screenwriter,
        critic
    ],
    max_iterations=5,
)

box_office_researcher = Agent(
    name="box_office_researcher",
    model=Gemini(model=model_name, retry_options=RETRY_OPTIONS),
    description="Considers the box office potential of this film",
    instruction="""
    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    INSTRUCTIONS:
    Write a report on the box office potential of a movie like that described in PLOT_OUTLINE based on the reported box office performance of other recent films.
    """,
    output_key="box_office_report"
)

casting_agent = Agent(
    name="casting_agent",
    model=Gemini(model=model_name, retry_options=RETRY_OPTIONS),
    description="Generates casting ideas for this film",
    instruction="""
    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    INSTRUCTIONS:
    Generate ideas for casting for the characters described in PLOT_OUTLINE
    by suggesting actors who have received positive feedback from critics and/or
    fans when they have played similar roles.
    """,
    output_key="casting_report"
)

preproduction_team = ParallelAgent(
    name="preproduction_team",
    sub_agents=[
        box_office_researcher,
        casting_agent
    ]
)

film_concept_team = SequentialAgent(
    name="film_concept_team",
    description="Write a film plot outline and save it as a text file.",
    sub_agents=[
        writers_room,
        preproduction_team,
        file_writer
    ],
)

root_agent = Agent(
    name="greeter",
    model=Gemini(model=model_name, retry_options=RETRY_OPTIONS),
    description="Guides user to create a movie idea.",
    instruction="""
    Ask the user for a historical figure.

    When user responds:
    - Store input in 'PROMPT' using append_to_state
    - Transfer to 'film_concept_team'
    """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[append_to_state],
    sub_agents=[film_concept_team],
)

# =========================
# APP SETUP
# =========================

graceful_plugin = Graceful429Plugin(
    name="graceful_429_plugin",
    fallback_text={
        "default": "**API quota exceeded. Please retry.**"
    }
)

graceful_plugin.apply_429_interceptor(root_agent)

app = App(
    name="workflow_agents",
    root_agent=root_agent,
    plugins=[graceful_plugin],
)
