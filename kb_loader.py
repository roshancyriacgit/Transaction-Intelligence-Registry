import json, pathlib

def load_kb(kb_dir:str):
    b=pathlib.Path(kb_dir)
    return {
        'schema': json.loads((b/'schemas'/'kb_schema.json').read_text(encoding='utf-8')),
        'rules': json.loads((b/'core'/'rules_demo.json').read_text(encoding='utf-8')),
        'forms': json.loads((b/'forms'/'forms_demo.json').read_text(encoding='utf-8')),
    }
