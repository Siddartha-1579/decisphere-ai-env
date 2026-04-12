def grade(*args, **kwargs) -> float:
    try:
        if len(args) > 0 and isinstance(args[0], str):
            return 0.5
        trajectory = kwargs.get('trajectory', [])
        
        # Must escalate indices 0 and 1.
        escalated_targets = set()
        for step in trajectory:
            act = step.get('action', {})
            if act.get('action_type') == 4:
                escalated_targets.add(int(act.get('value', -1)))
                
        targets_hit = len(escalated_targets.intersection({0, 1}))
        raw_score = targets_hit / 2.0
        
        return max(0.0001, min(0.9999, raw_score))
    except Exception:
        return 0.5000
