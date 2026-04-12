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

DeciSphere AI is a **real-world reinforcement learning benchmark environment** designed to evaluate how AI agents make **enterprise-level decisions** under constraints.

Unlike game-based RL environments, this system simulates **practical decision-making scenarios** focusing heavily on **Cascading Risk / Sequential Planning**. It tests an agent's ability to foresee downstream failure points such as:

* task prioritization
* resource allocation
* cascading risk management
* budget optimization
* time-sensitive workflows
* escalation strategies

---

## 🎯 Objective

The goal is to build a **deterministic, reproducible evaluation environment** where AI agents are scored based on:

* correctness of decisions
* efficiency (steps taken)
* risk management
* overall decision quality

---

## 🧩 Environment Design

The environment follows a Gym-like structure:

```python
reset() → initializes environment
step(action) → applies action
state() → returns current state
```

### 🔢 Action Space

Discrete actions:

| ID | Action     |
| -- | ---------- |
| 0  | prioritize |
| 1  | delay      |
| 2  | allocate   |
| 3  | ignore     |
| 4  | escalate   |

---

## 📊 State Representation

The environment returns a **fixed-length normalized numeric vector (~20 features)** including:

* task urgency & importance
* resource availability
* budget remaining
* risk level
* time remaining
* escalation count
* task queue signals

All values are normalized between **0 and 1**.

---

## 🧠 Tasks (Deterministic)

### ✅ Task 1 — Task Prioritization (Easy)

* Input: tasks with urgency & importance scores
* Rule: deterministic ranking using urgency × importance
* Goal: select optimal priority order

---

### ⚙️ Task 2 — Resource Allocation (Medium)

* Input: budget + project list (cost, value)
* Rule: knapsack-like optimal allocation
* Goal: maximize total value under constraints

---

### 🔥 Task 3 — Crisis Management (Hard)

* Input: dependency graph + cascading risk
* Rule: deterministic resolution sequence
* Goal: minimize global risk while resolving dependencies

---

## 🧮 Grading System

Each task uses a **deterministic programmatic grader**.

Scores are computed using:

* correctness
* efficiency
* decision quality
* risk handling

### ⚠️ IMPORTANT

All scores are **strictly bounded within (0, 1)**:

```python
score = max(0.0001, min(0.9999, score))
```

This ensures full compatibility with OpenEnv validation.

---

## 🎯 Reward System

Rewards are:

* normalized
* deterministic
* strictly between (0,1)

Includes:

* correctness reward
* efficiency bonus
* risk penalty
* delay penalty
* escalation penalty

---

## 🌐 API Endpoints

Backend is powered by FastAPI:

### 🔹 Reset Environment

```bash
GET /reset
```

### 🔹 Take Action

```bash
GET /step/{action}
```

### 🔹 Health Check

```bash
GET /
```

---

## 📦 Project Structure

```
decision-env/
├── environment.py
├── grader.py
├── agent.py
├── inference.py
├── openenv.yaml
├── Dockerfile
├── requirements.txt
├── server/
│   └── app.py
├── tasks/
│   ├── task1/
│   ├── task2/
│   └── task3/
```

---

## 🧪 Inference

The project includes an `inference.py` script that:

* interacts with the environment
* simulates agent decisions
* logs execution in structured format

```
[START]
[STEP]
[END]
```

---

## 🧰 Deployment

### ▶️ Run Locally

Backend:

```bash
cd server
uvicorn app:app --reload --port 7860
```

---

### 🤗 Hugging Face Spaces

This project is deployed using:

* **SDK:** Docker
* **Entry:** Dockerfile

---

## 🏆 Benchmark Goal

DeciSphere AI serves as a **scalable evaluation platform** for:

* RL agents
* rule-based systems
* LLM-based decision agents

It provides a **real-world benchmark** for measuring AI decision intelligence.

---

## 📌 Key Highlights

✅ Deterministic environment
✅ Multi-domain decision tasks
✅ Programmatic grading
✅ Validator-safe scoring
✅ API-based interaction
✅ Production-ready design

---

## 🔥 Final Note

This project is designed to feel like a **real enterprise AI benchmarking system**, not just a prototype.

It emphasizes:

* reliability
* reproducibility
* clarity
* real-world applicability

---

🚀 Built for the **Meta × Hugging Face OpenEnv Hackathon**
