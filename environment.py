from models import Observation

class DecisionEnv:
    def __init__(self):
        self.task_id = 1
        self.reset()
        
    def _initialize_task_data(self):
        # Deterministic state based on exact task IDs.
        self.task_queue = [0.0] * 5
        self.budget_remaining = 1.0
        self.risk_level = 0.0
        self.time_remaining = 1.0
        self.resources = 1.0
        self.escalation_count = 0
        self.completed_tasks = 0
        self.total_reward = 0.0
        self.reward_history = []
        
        # Load specific deterministic vectors representing raw inputs
        if self.task_id == 1:
            # Task 1: Urgency * Importance
            # Indexes: 0..4 mapped to scores e.g., 0.9*0.8
            self.task_queue = [0.9, 0.4, 0.8, 0.5, 0.2]  # Sorted optimal targets: 0, 2, 3, 1, 4
        elif self.task_id == 2:
            # Task 2: Budget vs Cost
            self.budget_remaining = 1.0
            self.task_queue = [0.2, 0.4, 0.5, 0.1, 0.8]  # Costs
        elif self.task_id == 3:
            # Task 3: Cascading Crisis
            self.risk_level = 0.8
            self.task_queue = [0.9, 0.1, 0.1, 0.1, 0.1]  # Critical root dependency is index 0
        elif self.task_id == 4:
            # Task 4: Budget Optimization (balance channels)
            self.budget_remaining = 0.5
            self.task_queue = [0.5, 0.5, 0.5, 0.5, 0.5]  # Needs balanced allocation actions
        elif self.task_id == 5:
            # Task 5: Escalation Strategy
            self.risk_level = 0.9
            self.task_queue = [1.0, 1.0, 0.0, 0.0, 0.0]  # First two are unresolvable natively without escalation
        
    def reset(self, task_id: int = 1) -> Observation:
        self.task_id = task_id
        self.step_count = 0
        self._initialize_task_data()
        return self._get_obs()

    def _get_obs(self) -> Observation:
        # Strictly length 20, 0-1 bounded normalized floats.
        vec = [
            float(self.task_id) / 10.0, # Normalize 1-5 to 0.1-0.5
            min(1.0, float(self.step_count) / 20.0),
            max(0.0, min(1.0, float(self.resources))),
            max(0.0, min(1.0, float(self.risk_level))),
            max(0.0, min(1.0, float(self.budget_remaining))),
            max(0.0, min(1.0, float(self.time_remaining))),
            min(1.0, float(self.completed_tasks) / 10.0),
            0.0, # missed_deadlines disabled for strict deterministic
            min(1.0, float(self.escalation_count) / 5.0)
        ] + [max(0.0, min(1.0, float(q))) for q in self.task_queue]
        
        # Pad to exactly 20 elements
        while len(vec) < 20:
            vec.append(0.0)
            
        return Observation(vector=vec[:20])

    def state(self) -> dict:
        return self._get_obs().dict()
        
    def step(self, action_type: int, value: float):
        self.step_count += 1
        raw_reward = 0.0
        
        # Use value as the target task index (0 to 4)
        target_idx = int(value) if 0 <= int(value) < 5 else 0
        
        # Actions: 0 -> prioritize, 1 -> delay, 2 -> allocate, 3 -> ignore, 4 -> escalate
        if action_type == 0:  # prioritize
            if self.task_queue[target_idx] > 0.0:
                self.task_queue[target_idx] = 0.0
                self.completed_tasks += 1
                raw_reward += 0.5
                self.risk_level -= 0.1
        elif action_type == 1:  # delay
            self.risk_level += 0.1
            raw_reward -= 0.2
        elif action_type == 2:  # allocate
            if self.budget_remaining >= 0.1:
                self.budget_remaining -= 0.1
                self.resources += 0.2
                self.task_queue[target_idx] = max(0.0, self.task_queue[target_idx] - 0.2)
                raw_reward += 0.2
            else:
                raw_reward -= 0.5
        elif action_type == 3:  # ignore
            self.risk_level += 0.2
            raw_reward -= 0.5
        elif action_type == 4:  # escalate
            self.escalation_count += 1
            self.risk_level -= 0.2
            self.task_queue[target_idx] = 0.0
            raw_reward += 0.1
            
        # Global boundaries
        self.risk_level = max(0.0, min(1.0, self.risk_level))
        self.resources = max(0.0, min(1.0, self.resources))
        self.budget_remaining = max(0.0, min(1.0, self.budget_remaining))
        self.time_remaining = max(0.0, self.time_remaining - 0.05)
        
        # Done condition
        done = self.step_count >= 10 or self.time_remaining <= 0.0 or self.risk_level >= 1.0 or sum(self.task_queue) <= 0.0
        
        # Normalize reward strictly to 0.0001 - 0.9999 for API return standard
        normalized_reward = 0.5 + (raw_reward / 4.0) # Map [-2, +2] -> [0, 1] generically
        api_reward = max(0.0001, min(0.9999, normalized_reward))
        
        self.total_reward += api_reward
        self.reward_history.append(api_reward)

        info = {"msg": "Step executed successfully", "raw_reward": raw_reward}
        return self._get_obs(), api_reward, done, info
