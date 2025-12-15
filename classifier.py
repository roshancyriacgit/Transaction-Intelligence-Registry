def classify(intake:dict):
    t=intake['transaction']
    pts=sorted({p.get('party_type') for p in t.get('parties',[])})
    has_foreign= any(p=='foreign_entity' for p in pts)
    return {
        'transaction_type': t.get('transaction_type'),
        'asset_class': t.get('asset_class'),
        'state': t.get('location',{}).get('state'),
        'timing': t.get('timing'),
        'party_types': pts,
        'has_foreign_party': has_foreign,
    }
