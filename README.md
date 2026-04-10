---
title: DeciSphere AI
emoji: 🤖
colorFrom: indigo
colorTo: blue
sdk: docker
sdk_version: "latest"
python_version: "3.10"
app_file: server/app.py
pinned: false
---

# 🧠 DeciSphere AI — DecisionEnv

A **Multi-Domain AI Decision-Making Benchmark Environment** built for the  
**Meta PyTorch Hackathon x Scaler School of Technology**.

This project evaluates how well AI agents make real-world decisions across:

- Task Prioritization
- Resource Allocation
- Risk Management
- Crisis Handling

---

## 🚀 Project Overview

DeciSphere AI is a **production-grade reinforcement learning environment** designed to simulate enterprise decision-making scenarios.

Agents interact with the environment by choosing actions such as:

- `prioritize`
- `delay`
- `allocate`
- `ignore`
- `escalate`

The environment dynamically updates:

- Risk levels
- Budget constraints
- Task queues
- Time pressure

---

## ⚙️ Environment API

The backend exposes a simple REST API:

### Reset Environment
`POST /reset?task_id=task1`
Resets the environment constraints safely formatted to OpenEnv specifications.

### Step Environment
`POST /step`
Payload contains:
```json
{
  "action_type": 1,
  "value": 1.0
}
```

---

## 🛠️ Setup and Usage
1. `pip install -r requirements.txt`
2. Start Server: `python -m uvicorn server.app:app`
3. Run inference baseline: `python inference.py`

## 🛡️ Validation Checking
We implemented highly defensive grader architectures capable of resolving OpenEnv strict validation string tests reliably while cleanly outputting constrained scores bounded strictly between `[0.0001 - 0.9999]`.
