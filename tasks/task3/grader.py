def grade(*args, **kwargs) -> float:
    try:
        if len(args) > 0 and isinstance(args[0], str):
            return 0.5
            
        trajectory = kwargs.get('trajectory', [])
        
        # Grading logic for Task 3 (Crisis Management)
        escalate_count = sum(1 for step in trajectory if step.get('action', {}).get('action_type') == 4)
        
        if len(trajectory) == 0:
            final_score = 0.3
        else:
            final_score = escalate_count / len(trajectory)
            
        return max(0.0001, min(0.9999, final_score))
        
    except Exception:
        return 0.5
