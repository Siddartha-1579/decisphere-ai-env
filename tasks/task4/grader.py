def grade(*args, **kwargs) -> float:
    try:
        if len(args) > 0 and isinstance(args[0], str):
            return 0.5
        trajectory = kwargs.get('trajectory', [])
        
        # We want to see 5 allocations distributed across indices 0,1,2,3,4.
        allocations = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        for step in trajectory:
            act = step.get('action', {})
            if act.get('action_type') == 2:
                idx = int(act.get('value', -1))
                if idx in allocations:
                    allocations[idx] += 1
                    
        balanced_count = sum(1 for v in allocations.values() if v == 1)
        raw_score = balanced_count / 5.0
        return max(0.0001, min(0.9999, raw_score))
    except Exception:
        return 0.5000
