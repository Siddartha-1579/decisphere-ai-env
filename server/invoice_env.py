import random
from typing import Dict, Any, Tuple
from models import Action, Observation

class DecisionEnv:
    def __init__(self):
        self.state_data = {}
        self.max_steps = 10
        self.reset("task1")
    
    def reset(self, task_id: str = "task1") -> Observation:
        random.seed(int(task_id[-1]) if task_id and task_id[-1].isdigit() else 42)
        
        domain_modifier = 1.0
        if "task2" in task_id: domain_modifier = 2.0
        elif "task3" in task_id: domain_modifier = 3.0
        elif "task4" in task_id: domain_modifier = 4.0
        elif "task5" in task_id: domain_modifier = 5.0
        
        self.state_data = {
            "task_id": domain_modifier,
            "step_count": 0.0,
            "resources": 100.0,
            "risk_level": 0.5,
            "budget_remaining": 1000.0,
            "time_remaining": self.max_steps * 1.0,
            "task_queue_size": 5.0,
            "completed_tasks": 0.0,
            "missed_deadlines": 0.0,
            "escalation_count": 0.0
        }
        return self.state()

    def state(self) -> Observation:
        vector = [
            float(self.state_data.get("task_id", 1.0)),
            float(self.state_data.get("step_count", 0.0)),
            float(self.state_data.get("resources", 100.0)),
            float(self.state_data.get("risk_level", 0.5)),
            float(self.state_data.get("budget_remaining", 1000.0)),
            float(self.state_data.get("time_remaining", 10.0)),
            float(self.state_data.get("task_queue_size", 5.0)),
            float(self.state_data.get("completed_tasks", 0.0)),
            float(self.state_data.get("missed_deadlines", 0.0)),
            float(self.state_data.get("escalation_count", 0.0))
        ]
        # Pad to robust length 20
        while len(vector) < 20:
            vector.append(0.0)
        return Observation(vector=vector)

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        self.state_data["step_count"] += 1.0
        self.state_data["time_remaining"] -= 1.0
        
        reward = 0.0
        act_type = action.action_type
        
        if act_type == 0: # prioritize
            self.state_data["task_queue_size"] = max(0.0, self.state_data["task_queue_size"] - 1.0)
            self.state_data["completed_tasks"] += 1.0
            reward = 0.8
        elif act_type == 1: # delay
            self.state_data["risk_level"] = min(1.0, self.state_data["risk_level"] + 0.15)
            self.state_data["missed_deadlines"] += 1.0
            reward = -0.2
        elif act_type == 2: # allocate
            self.state_data["resources"] -= 15.0
            self.state_data["budget_remaining"] -= 100.0
            self.state_data["task_queue_size"] = max(0.0, self.state_data["task_queue_size"] - 1.0)
            self.state_data["completed_tasks"] += 1.0
            reward = 1.0
        elif act_type == 3: # ignore
            self.state_data["risk_level"] = min(1.0, self.state_data["risk_level"] + 0.3)
            self.state_data["missed_deadlines"] += 1.0
            reward = -0.5
        elif act_type == 4: # escalate
            self.state_data["escalation_count"] += 1.0
            self.state_data["task_queue_size"] = max(0.0, self.state_data["task_queue_size"] - 1.0)
            reward = 0.2
        else:
            reward = -1.0 # unknown action
            
        # Contextual Modifiers
        if self.state_data["risk_level"] >= 0.8:
            reward -= 0.5
        if self.state_data["budget_remaining"] < 0:
            reward -= 1.0
            
        # End logic
        done = bool(self.state_data["step_count"] >= self.max_steps or self.state_data["task_queue_size"] <= 0)
        
        if self.state_data["task_queue_size"] <= 0:
            reward += 2.0 # Completion bonus

        # Reward range typically [-3, +3]
        reward = max(-3.0, min(3.0, float(reward)))
        
        info = {
            "state_data": self.state_data.copy()
        }
        
        return self.state(), reward, done, info
