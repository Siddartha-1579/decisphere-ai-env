# DeciSphere AI — Multi-Domain AI Decision Intelligence Benchmark

## Project Overview
DeciSphere AI is a complete production-grade OpenEnv benchmark for evaluating reinforcement learning and LLM agents in realistic enterprise decision-making workflows.

## Environment Design
Real-world operational decisions depend on efficient resource allocation, strategic delay, appropriate prioritization, and timely escalation. This benchmark mathematically models 5 tasks within this paradigm.

**Action Space (Discrete: 0-4):**
- `0`: Prioritize
- `1`: Delay
- `2`: Allocate
- `3`: Ignore
- `4`: Escalate

**Observation Space:** 
The environment yields a deterministically calculated vector dictating resources, budget, and task priority queues.

## Setup and Usage
1. `pip install -r requirements.txt`
2. Start Server: `python -m uvicorn server.app:app`
3. Run inference baseline: `python inference.py`

## Validation Checking
We implemented highly defensive grader architectures capable of resolving openenv `openenv validate` tests reliably while cleanly outputting standard clamped values of `[0.0001 - 0.9999]`.
