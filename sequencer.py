def sequence_steps(applicable_rules:list):
    out=[]
    for r in applicable_rules:
        for s in r.get('steps',[]):
            out.append({'rule_id': r['id'], 'step': s})
    return out
