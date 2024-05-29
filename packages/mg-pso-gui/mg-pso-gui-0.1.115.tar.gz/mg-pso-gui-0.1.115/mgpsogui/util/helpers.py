def extract_final_round_values(data):
    max_rounds = data['max_rounds'] + 1
    steps = data['n_steps'] + 1
    
    final_value = {}
    
    for round in range(max_rounds):
        for step in range(steps):
            key = f"r{round}s{step}"
            if key in data:
                obj = data[key] 
                round_steps = []
                for o_step in obj['steps']:
                    step_obj = {}
                    for param in o_step['param']:
                        if 'name' in param and 'value' in param:
                            step_obj[param['name']] = param['value']

                    round_steps.append(step_obj)
                final_value["data"] = round_steps
                final_value["index"] = key
    return final_value