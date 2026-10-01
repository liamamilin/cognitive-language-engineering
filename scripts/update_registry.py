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

def parse_model_cards(text):
    """Read legacy headings and reader-facing bilingual headings by stable ID."""
    pattern = r'^#{2,3} (?:(?P<old_id>[RCIA]-[PC]\d+)\. (?P<old_name>[^\n]+)|(?P<zh>[^\n]+)（(?P<en>[^\n]+)） · (?P<new_id>[RCIA]-[PC]\d+))\n'
    cards = []
    for match in re.finditer(pattern, text, re.M):
        next_heading = re.search(r'^#{2,3} ', text[match.end():], re.M)
        end = match.end() + next_heading.start() if next_heading else len(text)
        cards.append({
            'id': match['old_id'] or match['new_id'],
            'name': match['old_name'] or match['en'],
            'display_name': match['zh'] or match['old_name'],
            'body': text[match.end():end],
        })
    return cards

def parse_registry():
    records = []
    for model in ['M1', 'M2', 'M3', 'M4']:
        text = (ROOT / f'docs/models/{model}.md').read_text()
        for card in parse_model_cards(text):
            ident, name, body = card['id'], card['name'], card['body']
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
