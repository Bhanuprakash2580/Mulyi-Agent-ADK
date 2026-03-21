# 🤖 Build Multi-Agent Systems with ADK — Google Cloud

> **Platform:** Google Cloud | **Lab:** Build Multi-Agent Systems with ADK (GENAI106)
> **Duration:** 1 hour 30 minutes | **Completed:** March 2026

---

## 📌 Overview

This project documents my completion of the **Build Multi-Agent Systems with ADK** hands-on lab on Google Cloud. I built a sophisticated multi-agent system using the **Google Agent Development Kit (ADK)** — orchestrating multiple AI agents that collaborate, communicate through session state, and execute complex workflows to autonomously produce a complete movie pitch document including plot outline, box office analysis, and casting suggestions.

---

## 🎯 What I Built

| Component | Description |
|-----------|-------------|
| **Parent & Sub-Agent System** | Hierarchical agent tree with a root agent transferring conversations to specialist sub-agents |
| **Session State Management** | Used ToolContext to store and retrieve data across multiple agents in real time |
| **SequentialAgent Pipeline** | Linear research → write → save workflow for movie pitch generation |
| **LoopAgent — Writers Room** | Iterative loop of researcher → screenwriter → critic refining output across multiple passes |
| **ParallelAgent — Pre-production Team** | box_office_researcher and casting_agent running simultaneously for faster results |
| **Complete Movie Pitch Pipeline** | End-to-end autonomous system producing plot outline + box office report + casting report |

---

## 🏗️ System Architecture — Evolution

### Stage 1 — Hierarchical Agent Tree (Concept)

The foundation of ADK — organizing agents in a tree structure where root_agent delegates to sub-agents at each level.

![Hierarchical Agent Tree](screenshots/The_Hierarchical_Agent_Tree.png)

---

### Stage 2 — SequentialAgent Pipeline (Task 4)

The first working version: greeter → researcher (Wikipedia) → screenwriter → file_writer running in sequence.

![Sequential Agent Pipeline](screenshots/building_a_multi-agent_system_with_a_SequentialAgent.png)

---

### Stage 3 — LoopAgent Added (Task 5)

The writers_room LoopAgent wraps researcher → screenwriter → critic in an iterative loop. The critic decides whether to keep iterating or call `exit_loop` when the outline is good enough.

![Loop Agent System](screenshots/LoopAgent_for_iterative_work.png)

---

### Stage 4 — Full System with ParallelAgent (Task 6) ⭐

The complete final architecture — SequentialAgent containing a LoopAgent + ParallelAgent running box_office_researcher and casting_agent simultaneously, then file_writer aggregating everything.

![Full Multi-Agent System](screenshots/pattern_for_report_generation_with_a_ParallelAgent.png)

---

## 📋 Final Architecture Summary

```
greeter (root_agent)
│
└── film_concept_team (SequentialAgent)
    │
    ├── writers_room (LoopAgent) ← iterates up to 5x
    │   ├── researcher        → wikipedia tool
    │   ├── screenwriter      → writes plot outline
    │   └── critic            → exit_loop tool (decides when done)
    │
    ├── preproduction_team (ParallelAgent) ← runs both simultaneously
    │   ├── box_office_researcher  → estimates box office results
    │   └── casting_agent          → generates casting ideas
    │
    └── file_writer  → aggregates all output → writes .txt file
```

---

## 📸 Lab Screenshots

### 1. ADK Installation — Environment Setup
Successfully installed Google ADK and all requirements in Cloud Shell Terminal.

![ADK Installation](screenshots/ADK_Installation.png)

---

### 2. agent.py — Code in Cloud Shell Editor
The agent.py file open in Cloud Shell Editor showing the multi-agent system code.

![Agent Code](screenshots/Agent_Code_Editor.png)

---

### 3. CLI — Parent to Sub-Agent Transfer
Terminal showing [steering] root agent transferring to [travel_brainstormer] sub-agent automatically.

![CLI Agent Transfer](screenshots/CLI_Agent_Transfer.png)

---

### 4. CLI — Peer Agent Transfer
Terminal showing transfer from [attractions_planner] to [travel_brainstormer] — peer agent transfer working.

![Peer Agent Transfer](screenshots/CLI_Peer_Agent_Transfer.png)

---

### 5. ADK Web UI — Session State Tab
The State tab showing the attractions array being updated in real time as the agent saves user selections.

![Session State](screenshots/Session_State_Tab.png)

---

### 6. Session State — state_delta Tool Event
The tool response event showing the state_delta field — the tool successfully updated the session state dictionary.

![State Delta](screenshots/State_Delta_Event.png)

---

### 7. ADK Web UI — Agent Tree Graph (Task 4)
Visual graph showing the SequentialAgent pipeline in the ADK Dev UI.

![Agent Tree Task 4](screenshots/Agent_Tree_Sequential.png)

---

### 8. Generated Movie Pitch File — Task 4 Output
The AI-generated .txt file written to disk by the file_writer after the SequentialAgent pipeline completes.

![Movie Pitch File](screenshots/Movie_Pitch_File_Task4.png)

---

### 9. LoopAgent — Iterations in Web UI Sidebar
The event sidebar showing researcher → screenwriter → critic repeating across multiple loop iterations.

![Loop Agent Iterations](screenshots/Loop_Agent_Iterations.png)

---

### 10. Critic Agent — exit_loop Tool Called
The critic agent deciding the outline meets all criteria and calling exit_loop to end the iteration.

![Exit Loop](screenshots/Critic_Exit_Loop.png)

---

### 11. Improved Movie Pitch — After Loop Refinement
Refined output after multiple iterations — showing improved quality vs the Task 4 single-pass version.

![Improved Pitch](screenshots/Improved_Movie_Pitch.png)

---

### 12. ⭐ Full Agent Tree — All 3 Workflow Agents
Complete system graph showing Sequential + Loop + Parallel agents all together in the ADK Dev UI.

![Full Agent Tree](screenshots/Full_Agent_Tree_All_Agents.png)

---

### 13. ParallelAgent — Concurrent Execution
preproduction_team ParallelAgent running box_office_researcher and casting_agent simultaneously.

![Parallel Agent](screenshots/Parallel_Agent_Running.png)

---

### 14. Final Output — Complete Movie Pitch Document
The complete output file with all three sections: Plot Outline + Box Office Report + Casting Report.

![Final Output](screenshots/Final_Movie_Pitch_Complete.png)

---

## 🧠 Key Concepts Demonstrated

### Multi-Agent Architecture
- Hierarchical agent trees with parent → sub-agent relationships
- Peer agent transfers between specialist agents
- Root agent orchestrating the full conversation flow

### Session State Management
- `ToolContext` for reading and writing to session state across agents
- `state_delta` tracking real-time state changes per tool event
- Key templating (`{ key? }`) injecting state values into agent instructions
- `output_key` parameter storing full agent responses in state automatically

### Workflow Agents
- **SequentialAgent** — linear task pipelines where each agent's output feeds the next
- **LoopAgent** — iterative refinement with `exit_loop` tool for intelligent termination
- **ParallelAgent** — concurrent execution of independent tasks for faster results

### Tools Used
- `wikipedia` — LangChain Wikipedia tool for real-time research
- `append_to_state` — custom tool for accumulating content across loop iterations
- `exit_loop` — built-in ADK tool for intelligent loop termination by the critic
- `write_file` — custom tool for writing final output to disk

---

## 🔧 Technologies Used

`Google Cloud` `Google Agent Development Kit (ADK)` `Vertex AI` `Gemini` `Python` `LangChain` `Cloud Shell`

---

## 📁 Project Structure

```
adk_multiagent_systems/
│
├── parent_and_subagents/
│   ├── agent.py          ← Task 2 & 3: transfers + session state
│   └── .env
│
├── workflow_agents/
│   ├── agent.py          ← Task 4, 5 & 6: Sequential, Loop, Parallel
│   └── .env
│
└── movie_pitches/        ← AI-generated output files
    └── *.txt
```

---

## 💡 Key Learning Outcomes

- Building reliable multi-step AI behaviors without complex single prompts
- Dividing tasks across specialized agents for better performance and maintainability
- Using session state as a shared memory layer across multiple agents
- Controlling agent flow with Sequential, Loop, and Parallel workflow patterns
- Agents making intelligent autonomous decisions — the critic deciding when to exit the loop

---

## 📄 Lab Details

- **Lab Name:** Build Multi-Agent Systems with ADK (GENAI106)
- **Platform:** Google Cloud Skills Boost (Qwiklabs)
- **Duration:** 1 hour 30 minutes | **Credits:** 7
- **Prerequisites:** Get started with Google ADK · Empower ADK agents with tools

---

*Part of my Google Cloud AI & Agent Development learning journey.*
