from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models import Action, StepResponse, ResetResponse, StateResponse
from environment import DecisionEnv
import uvicorn
import sys

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

@app.post("/reset", response_model=ResetResponse)
def reset_env(task_id: str = Query("task1")):
    try:
        t_id = int(task_id.replace("task", ""))
    except ValueError:
        t_id = 1
        
    obs = env.reset(task_id=t_id)
    return ResetResponse(observation=obs, info={"msg": "Environment reset"})

@app.post("/step", response_model=StepResponse)
def step_env(action: Action):
    obs, reward, done, info = env.step(action.action_type, action.value)
    return StepResponse(observation=obs, reward=reward, done=done, info=info)

@app.get("/state", response_model=StateResponse)
def state_env():
    return StateResponse(state=env.state())

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()
