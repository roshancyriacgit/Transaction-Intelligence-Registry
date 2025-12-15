def rule_applies(rule:dict, c:dict)->bool:
    cond=rule.get('applies_if',{})
    if 'transaction_type' in cond and c.get('transaction_type') not in cond['transaction_type']:
        return False
    if 'asset_class' in cond and c.get('asset_class') not in cond['asset_class']:
        return False
    if 'party_type' in cond:
        pts=set(c.get('party_types',[]))
        if not any(pt in pts for pt in cond['party_type']):
            return False
    return True

def select_applicable(rules:list, c:dict):
    return [r for r in rules if rule_applies(r,c)]
