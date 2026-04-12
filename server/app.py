import sys
import os

# Add root directory to sys.path so we can import from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from models import Action, StepResponse, ResetResponse, StateResponse, ResetRequest
from environment import DecisionEnv
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

env = DecisionEnv()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "DeciSphere AI Benchmark Server"}

@app.get("/reset")
@app.post("/reset", response_model=ResetResponse)
def reset_env(req: Optional[ResetRequest] = None, task_id: Optional[str] = Query(None)):
    final_task = "task1"
    if req and getattr(req, "task_id", None):
        final_task = req.task_id
    elif task_id:
        final_task = task_id
        
    try:
        t_id = int(str(final_task).replace("task", ""))
    except ValueError:
        t_id = 1
        
    obs = env.reset(task_id=t_id)
    return ResetResponse(observation=obs, info={"msg": "Environment reset"})

@app.get("/step/{action}")
def step_env_get(action: int, value: float = Query(0.0)):
    obs, api_reward, done, info = env.step(action, value)
    
    # Run dynamic correctness explicitly for logging if needed or just bound 
    # the info into the requested schema perfectly:
    return {
        "step": env.step_count,
        "max_steps": 10,
        "total_reward": env.total_reward,
        "risk_level": env.risk_level,
        "budget_remaining": env.budget_remaining,
        "correctness": api_reward, 
        "escalations_used": env.escalation_count,
        "reward_history": env.reward_history,
        "action_distribution": {},
        "task_name": f"task{env.task_id}",
        "done": done
    }

@app.post("/step", response_model=StepResponse)
def step_env(action: Action):
    obs, reward, done, info = env.step(action.action_type, action.value)
    info["step"] = env.step_count
    info["max_steps"] = 10
    info["total_reward"] = env.total_reward
    info["risk_level"] = env.risk_level
    info["budget_remaining"] = env.budget_remaining
    info["correctness"] = reward
    info["escalations_used"] = env.escalation_count
    info["reward_history"] = env.reward_history
    info["action_distribution"] = {}
    info["task_name"] = f"task{env.task_id}"
    
    return StepResponse(observation=obs, reward=reward, done=done, info=info)

@app.get("/state", response_model=StateResponse)
def state_env():
    return StateResponse(state=env.state())

def main():
    # Because we added the root dir to sys.path and this is being run as `python server/app.py`,
    # the module `server.app:app` won't be found by uvicorn since uvicorn runs its own import system
    # from the working directory. To natively support `python server/app.py` we can either run
    # `app:app` if run from within server directory, or just import app and run it differently.
    # However, uvicorn works with string "server.app:app" if the CWD is the root.
    # OpenEnv normally runs python from the root directory but calls "python server/app.py".
    # But let's support both properly by getting the root path:
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False, app_dir=root_dir)

if __name__ == "__main__":
    main()
