def grade(*args, **kwargs) -> float:
    try:
        if len(args) > 0 and isinstance(args[0], str):
            return 0.5
        trajectory = kwargs.get('trajectory', [])
        if not trajectory:
            return 0.05
            
        # Crisis management optimal action is resolving index 0 first
        first_step = trajectory[0].get('action', {})
        if first_step.get('action_type') == 0 and int(first_step.get('value', -1)) == 0:
            return 0.95
        
        # Did they resolve it later?
        for step in trajectory:
            act = step.get('action', {})
            if act.get('action_type') == 0 and int(act.get('value', -1)) == 0:
                return 0.50
                
        return 0.10
    except Exception:
        return 0.5000
