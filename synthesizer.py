from datetime import datetime

def synthesize(case_id:str, intake:dict, c:dict, applicable:list, steps:list):
    filings=[]
    for r in applicable:
        for f in r.get('forms',[]):
            filings.append({'rule_id': r['id'], 'authority': f.get('authority'), 'form': f.get('form'), 'timing': f.get('timing')})
    structure=[]
    if c.get('transaction_type') in ('investment','loan'):
        structure += [
            'Route option: staged funding/transfer with conditions and verification checkpoints.',
            'Risk control: consider escrow/holdback where timing risk is high.'
        ]
    if c.get('asset_class')=='immovable_property':
        structure.append('Route option: title verification + stamp + registration sequencing before final release of consideration.')
    if c.get('has_foreign_party'):
        structure.append('Route option: include foreign investment reporting pathway and route/cap checks (verify).')
    return {
        'case_id': case_id,
        'generated_at': datetime.utcnow().isoformat()+'Z',
        'intent': intake['transaction'],
        'classification': c,
        'structure_options': structure or ['Route options generated from intent + rule packs.'],
        'applicable_rule_packs': [{'id': r['id'], 'title': r['title'], 'domain': r['domain'], 'trigger': r.get('trigger'), 'risk_flags': r.get('risk_flags',[])} for r in applicable],
        'execution_plan': steps,
        'filings_checklist': filings,
        'tir_record': {
            'principle': 'TIR surfaces references + sequencing; users/professionals decide final actions.',
            'traceability': 'Each output item references a rule_id; full build adds provenance + versioned KB snapshots.'
        },
        'disclaimer': 'Illustrative reference output; verify statutes/forms/timelines.'
    }
