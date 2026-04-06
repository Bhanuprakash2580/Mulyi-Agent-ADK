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

<img width="838" height="357" alt="The Hierarchical Agent Tree" src="https://github.com/user-attachments/assets/b2bbec2c-dc1e-4420-a8de-bab3b4212762" />

---

### Stage 2 — SequentialAgent Pipeline (Task 4)

The first working version: greeter → researcher (Wikipedia) → screenwriter → file_writer running in sequence.

<img width="2112" height="960" alt="building a multi-agent system with a SequentialAgent" src="https://github.com/user-attachments/assets/9b9e9ba9-cf3c-469c-bafb-e9fd90b1c5d1" />

---

### Stage 3 — LoopAgent Added (Task 5)

The writers_room LoopAgent wraps researcher → screenwriter → critic in an iterative loop. The critic decides whether to keep iterating or call `exit_loop` when the outline is good enough.

<img width="2112" height="960" alt="LoopAgent for iterative work" src="https://github.com/user-attachments/assets/eaec5f56-51c8-4be8-9723-628b6be70001" />

---

### Stage 4 — Full System with ParallelAgent (Task 6) ⭐

The complete final architecture — SequentialAgent containing a LoopAgent + ParallelAgent running box_office_researcher and casting_agent simultaneously, then file_writer aggregating everything.

<img width="2112" height="960" alt="pattern for report generation with a ParallelAgent" src="https://github.com/user-attachments/assets/efed67b3-34c3-42eb-bcf4-64d06f857d19" />

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

<img width="2560" height="1528" alt="Screenshot 2026-03-20 210207" src="https://github.com/user-attachments/assets/2e57aa6a-902a-4c66-9456-ab8893f5a5d4" />

---

### 2. agent.py — Code in Cloud Shell Editor
The agent.py file open in Cloud Shell Editor showing the multi-agent system code.

<img width="2560" height="1528" alt="Screenshot 2026-03-20 210458" src="https://github.com/user-attachments/assets/79ff4f1f-2bcf-4676-bab7-497c14b29d33" />

---

### 3. CLI — Parent to Sub-Agent Transfer
Terminal showing [steering] root agent transferring to [travel_brainstormer] sub-agent automatically.

<img width="1856" height="949" alt="Screenshot 2026-03-20 211329" src="https://github.com/user-attachments/assets/2daef708-8c6c-42f6-9660-0a0f20e0b422" />

---

### 4. CLI — Peer Agent Transfer
Terminal showing transfer from [attractions_planner] to [travel_brainstormer] — peer agent transfer working.

<img width="1859" height="1090" alt="Screenshot 2026-03-20 212504" src="https://github.com/user-attachments/assets/54f2a93d-001a-4d39-8fe1-0e7250c49fd2" />

---

### 5. ADK Web UI — Session State Tab
The State tab showing the attractions array being updated in real time as the agent saves user selections.

<img width="2560" height="1600" alt="Screenshot 2026-03-20 213620" src="https://github.com/user-attachments/assets/3c4366c5-e089-452d-ab86-45f8e013fac4" />

---

### 6. Session State — state_delta Tool Event
The tool response event showing the state_delta field — the tool successfully updated the session state dictionary.

<img width="2560" height="1600" alt="Screenshot 2026-03-20 213648" src="https://github.com/user-attachments/assets/464edcd4-427b-45bf-a59f-7f5055b89d9a" />

---

### 7. ADK Web UI — Agent Tree Graph (Task 4)
Visual graph showing the SequentialAgent pipeline in the ADK Dev UI.

<img width="2560" height="1600" alt="Screenshot 2026-03-20 214840" src="https://github.com/user-attachments/assets/be508c54-4619-48eb-a072-48eb9b12d190" />

---

### 8. Generated Movie Pitch File — Task 4 Output
The AI-generated .txt file written to disk by the file_writer after the SequentialAgent pipeline completes.

<img width="2560" height="1600" alt="Screenshot 2026-03-20 215104" src="https://github.com/user-attachments/assets/65560b8f-7d98-4617-8fd4-b38854a42004" />

---

### 9. LoopAgent — Iterations in Web UI Sidebar
The event sidebar showing researcher → screenwriter → critic repeating across multiple loop iterations.

<img width="2560" height="1600" alt="Screenshot 2026-03-20 224052" src="https://github.com/user-attachments/assets/e935be40-be7b-4e99-98fc-9a95388bbd8d" />

---

### 10. Critic Agent — exit_loop Tool Called
The critic agent deciding the outline meets all criteria and calling exit_loop to end the iteration.

<img width="2560" height="1600" alt="Screenshot 2026-03-20 225556" src="https://github.com/user-attachments/assets/f527da25-a02d-4a65-9b0a-198bcb7a37d2" />

---

### 11. Improved Movie Pitch — After Loop Refinement
Refined output after multiple iterations — showing improved quality vs the Task 4 single-pass version.

<img width="2560" height="1600" alt="Screenshot 2026-03-20 225813" src="https://github.com/user-attachments/assets/de52b84e-aa8c-442c-8d7b-34ba7dcb086d" />

---

### 12. ⭐ Full Agent Tree — All 3 Workflow Agents
Complete system graph showing Sequential + Loop + Parallel agents all together in the ADK Dev UI.

<img width="2560" height="1600" alt="Screenshot 2026-03-20 230743" src="https://github.com/user-attachments/assets/36914035-beed-47e1-bb8c-121fc8836ca8" />

---

### 13. ParallelAgent — Concurrent Execution
preproduction_team ParallelAgent running box_office_researcher and casting_agent simultaneously.

<img width="2560" height="1600" alt="Screenshot 2026-03-20 230941" src="https://github.com/user-attachments/assets/d86ae0d4-7afc-430f-b685-b6108ec297d4" />

---

### 14. Final Output — Complete Movie Pitch Document
The complete output file with all three sections: Plot Outline + Box Office Report + Casting Report.

<img width="2560" height="1600" alt="Screenshot 2026-03-20 231230" src="https://github.com/user-attachments/assets/08bec080-74e8-4781-9cfd-97be2e4b2446" />


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


*Part of my Google Cloud AI & Agent Development learning journey.*
# Mulyi-Agent-ADK
