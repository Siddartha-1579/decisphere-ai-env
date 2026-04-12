---
title: DeciSphere AI
emoji: 🧠
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
---

# 🧠 DeciSphere AI — Multi-Domain Decision Intelligence Benchmark

## 🚀 Overview

DeciSphere AI is a real-world reinforcement learning benchmark environment designed to evaluate how well AI agents make business-critical decisions under constraints.

Unlike game environments, this system simulates practical enterprise scenarios such as:

📌 Task prioritization
💰 Resource allocation
⚠️ Risk & crisis management
⏳ Time & deadline handling
🚨 Escalation strategies

👉 The goal is to test decision intelligence, not gameplay.

## 🎯 Why This Matters

Modern AI systems struggle with multi-step reasoning under constraints.

DeciSphere AI provides a structured environment where agents must:

* balance competing priorities
* manage limited resources
* reduce risk dynamically
* make sequential decisions

This mirrors real-world use cases in:

* operations management
* project planning
* business strategy systems
* autonomous decision engines

## 🧩 Environment Design

### 🧠 State Representation

Each step provides a structured state including:

* task queue (top 5 tasks)
* urgency & importance
* available resources (budget, staff)
* risk level (0–1)
* time remaining
* completed / missed tasks
* escalation count

👉 All values are normalized into a fixed numeric vector (~20 features).

### 🎮 Action Space

The agent chooses from 5 actions:

| Action | Meaning |
| :--- | :--- |
| 0 | Prioritize task |
| 1 | Delay task |
| 2 | Allocate resources |
| 3 | Ignore task |
| 4 | Escalate issue |

## 🧪 Tasks (Increasing Difficulty)

### ✅ Task 1 — Task Prioritization (Easy)

Agent must select the most important and urgent tasks.

✔️ Tests:
* urgency vs importance reasoning
* scheduling decisions

### ⚖️ Task 2 — Resource Allocation (Medium)

Agent must distribute limited budget and time across projects.

✔️ Tests:
* optimization under constraints
* trade-off decisions

### 🔥 Task 3 — Crisis Management (Hard)

Agent handles cascading failures where decisions impact global risk.

✔️ Tests:
* sequential reasoning
* dependency handling
* risk minimization

## 🎯 Reward System

Rewards are dense and structured, encouraging intelligent behavior.

**Positive Signals:**
* correct decision → +reward
* task completion → bonus
* efficient actions → bonus

**Penalties:**
* increasing risk → penalty
* delaying urgent tasks → penalty
* ignoring critical tasks → penalty
* over-escalation → penalty

👉 Final rewards are strictly clamped between (0, 1) for validator compliance.

## 📊 Example Episode
Step 1 → Action: Prioritize → Reward: 0.72  
Step 2 → Action: Allocate → Reward: 0.65  
Step 3 → Action: Escalate → Reward: 0.81  

Final Score: 0.79

## 🧮 Grading System

Each task is evaluated using deterministic metrics:

* correctness
* efficiency
* decision quality
* risk management

👉 Final score is normalized to (0, 1) for all tasks.

## 🤖 Baseline Agents
* 🎲 **RandomAgent** — random decisions (control baseline)
* 📏 **RuleBasedAgent** — heuristic-driven decisions

## 🌐 API Endpoints

Backend is powered by FastAPI.

**Reset Environment**
`GET /reset`

**Take Action**
`GET /step/{action}`

## 🧪 Local Testing

Start backend:
```bash
uvicorn server.app:app --reload --port 7860
```

Test:
```bash
curl http://127.0.0.1:7860/reset
curl http://127.0.0.1:7860/step/0
```

## 🧠 Inference System

The `inference.py` script:

* interacts with the API
* runs multiple steps
* logs structured outputs
* evaluates agent performance

## 🐳 Deployment (Hugging Face Spaces)
* Docker-based deployment
* Fully reproducible environment
* API-ready inference

## 📁 Project Structure
```text
decision-env/
├── environment.py
├── grader.py
├── agent.py
├── inference.py
├── openenv.yaml
├── Dockerfile
├── README.md
├── server/
│   └── app.py
├── tasks/
```

## ✅ OpenEnv Compliance

✔️ Deterministic environment
✔️ Valid reward range (0,1)
✔️ API endpoints functional
✔️ Docker builds successfully
✔️ Inference reproducible

## 🏁 Conclusion

DeciSphere AI is not just an environment — it is a decision intelligence benchmark designed to push AI systems toward real-world reasoning capabilities.

It combines:

* structured environments
* multi-domain challenges
* meaningful reward shaping
* scalable evaluation

👉 Making it a strong candidate for evaluating next-generation AI decision systems.
