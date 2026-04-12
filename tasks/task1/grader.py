def grade(*args, **kwargs) -> float:
    try:
        if len(args) > 0 and isinstance(args[0], str):
            return 0.5
        trajectory = kwargs.get('trajectory', [])
        
        # Optimal sequence of indices for Task 1 Prioritization: 0, 2, 3, 1, 4
        optimal_order = [0, 2, 3, 1, 4]
        agent_order = []
        for step in trajectory:
            act = step.get('action', {})
            if act.get('action_type') == 0:
                agent_order.append(int(act.get('value', 0)))
                
        # Calculate matching score against optimal length prefix
        matches = 0
        for i, val in enumerate(agent_order):
            if i < len(optimal_order) and val == optimal_order[i]:
                matches += 1
                
        if len(optimal_order) == 0:
            raw_score = 0.5
        else:
            raw_score = matches / len(optimal_order)
            
        penalty = 0.05 * (len(trajectory) - matches) # Efficiency penalty
        final_score = raw_score - penalty
        return max(0.0001, min(0.9999, final_score))
        
    except Exception:
        return 0.5000
