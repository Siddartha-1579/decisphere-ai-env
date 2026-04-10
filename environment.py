import random
from models import Observation

class DecisionEnv:
    def __init__(self):
        self.seed = 42
        random.seed(self.seed)
        self.task_id = 1
        self.reset()
        
    def reset(self, task_id: int = 1) -> Observation:
        self.task_id = task_id
        self.step_count = 0
        self.resources = 1.0
        self.risk_level = 0.2
        self.budget_remaining = 1.0
        self.time_remaining = 1.0
        self.task_queue = [random.uniform(0, 1) for _ in range(5)]
        self.completed_tasks = 0
        self.missed_deadlines = 0
        self.escalation_count = 0
        return self._get_obs()

    def _get_obs(self) -> Observation:
        return Observation(
            task_id=self.task_id,
            step_count=self.step_count,
            resources=self.resources,
            risk_level=self.risk_level,
            budget_remaining=self.budget_remaining,
            time_remaining=self.time_remaining,
            task_queue=self.task_queue,
            completed_tasks=self.completed_tasks,
            missed_deadlines=self.missed_deadlines,
            escalation_count=self.escalation_count
        )

    def state(self) -> dict:
        return self._get_obs().dict()

    def step(self, action_type: int, value: float):
        self.step_count += 1
        reward = 0.0
        
        # Actions: 0 -> prioritize, 1 -> delay, 2 -> allocate, 3 -> ignore, 4 -> escalate
        if action_type == 0:  # prioritize
            if self.task_queue:
                self.task_queue.pop(0)
                self.task_queue.append(random.uniform(0, 1))
                self.completed_tasks += 1
                reward += 0.5
                self.risk_level = max(0.0, self.risk_level - 0.05)
            else:
                reward -= 0.1
        elif action_type == 1:  # delay
            self.missed_deadlines += 1
            self.risk_level = min(1.0, self.risk_level + 0.1)
            reward -= 0.2
        elif action_type == 2:  # allocate
            if self.budget_remaining >= 0.1:
                self.budget_remaining -= 0.1
                self.resources = min(1.0, self.resources + 0.2)
                reward += 0.2
            else:
                reward -= 0.5
        elif action_type == 3:  # ignore
            self.missed_deadlines += 1
            self.risk_level = min(1.0, self.risk_level + 0.15)
            reward -= 0.5
        elif action_type == 4:  # escalate
            self.escalation_count += 1
            self.risk_level = max(0.0, self.risk_level - 0.1)
            reward -= 0.1 # Slight penalty for not handling it
        else:
            reward -= 1.0 # Invalid action

        # Domain specific bonus/penalty based on task
        if self.task_id == 1 and action_type == 0:
            reward += 0.5
        elif self.task_id == 2 and action_type == 2:
            reward += 0.5
        elif self.task_id == 3 and self.risk_level > 0.8 and action_type == 4:
            reward += 1.0 # Great crisis management

        # Global time step decay
        self.time_remaining = max(0.0, self.time_remaining - 0.05)
        
        # Max steps or out of time
        done = self.step_count >= 20 or self.time_remaining <= 0.0 or self.risk_level >= 1.0

        info = {"msg": "Step executed successfully"}
        return self._get_obs(), reward, done, info
