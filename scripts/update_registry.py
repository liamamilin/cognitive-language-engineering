"""Derive the model registry from Markdown; no second editable specification."""
from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ID = r'(?:[RCIABO]-[PC]\d+|ME\d+)'

def field(body, label):
    match = re.search(r'\*\*' + re.escape(label) + r'：\*\* ([^\n]+)', body)
    return re.findall(r'\[(' + ID + r')\]', match[1]) if match else []

def parse_registry():
    records = []
    for model in ['M1', 'M2', 'M3', 'M4']:
        text = (ROOT / f'docs/models/{model}.md').read_text()
        parts = re.split(r'^## ([RCIA]-[PC]\d+)\. ([^\n]+)\n', text, flags=re.M)[1:]
        for i in range(0, len(parts), 3):
            ident, name, body = parts[i:i+3]
            specialization = field(body, '类型')
            records.append({
                'id': ident, 'model': model, 'name': name,
                'kind': 'Specialization' if specialization else ('Composite' if '-C' in ident else 'EngineeringPrimitive'),
                'specializes': specialization[0] if specialization else None,
                'components': field(body, '可复用组成'),
                'cross_domain': field(body, '跨域过程引用'),
                'mechanisms': field(body, '机制候选'),
            })
    return records

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    path = ROOT / 'scripts/registry_snapshot.json'
    expected = parse_registry()
    if args.check:
        actual = json.loads(path.read_text())
        if actual != expected:
            raise SystemExit('Registry snapshot differs from source: run update_registry.py')
        print(f'Registry matches source: {len(expected)} interfaces, all fields.')
    else:
        path.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + '\n')
        print(f'Registry snapshot updated from source: {len(expected)} interfaces.')
