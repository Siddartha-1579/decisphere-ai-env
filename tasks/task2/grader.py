def grade(*args, **kwargs) -> float:
    try:
        if len(args) > 0 and isinstance(args[0], str):
            return 0.5
        trajectory = kwargs.get('trajectory', [])
        
        # Optimal allocation targets for Task 2 costs [0.2, 0.4, 0.5, 0.1, 0.8] with budget 1.0
        # Optimal combo: 0, 1, 3 (sum=0.7).
        optimal_targets = {0, 1, 3}
        agent_allocations = set()
        penalty_steps = 0
        
        for step in trajectory:
            act = step.get('action', {})
            act_type = act.get('action_type')
            val = int(act.get('value', 0))
            if act_type == 2:
                agent_allocations.add(val)
            else:
                penalty_steps += 1
                
        correct_allocations = len(agent_allocations.intersection(optimal_targets))
        incorrect_allocations = len(agent_allocations - optimal_targets)
        
        raw_score = (correct_allocations / len(optimal_targets)) - (0.2 * incorrect_allocations) - (0.05 * penalty_steps)
        return max(0.0001, min(0.9999, raw_score))
    except Exception:
        return 0.5000
