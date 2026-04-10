from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class Observation(BaseModel):
    task_id: int
    step_count: int
    resources: float
    risk_level: float
    budget_remaining: float
    time_remaining: float
    task_queue: List[float]
    completed_tasks: int
    missed_deadlines: int
    escalation_count: int
    # Ensure it is a vector overall size ~14 elements

class Action(BaseModel):
    action_type: int = Field(..., ge=0, le=4, description="0=prioritize, 1=delay, 2=allocate, 3=ignore, 4=escalate")
    value: float = Field(0.0)

class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any]

class ResetResponse(BaseModel):
    observation: Observation
    info: Dict[str, Any]

class StateResponse(BaseModel):
    state: Dict[str, Any]
