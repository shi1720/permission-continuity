"""Audit a reviewed JSON portfolio; unresolved evidence blocks a coverage claim.

Usage: python3 -m src.check_portfolio data/example_portfolio.json
"""
import argparse, json
from pathlib import Path
from src.continuity import Window, audit

def check(spec):
    problems=[]; paths=[]
    for path in spec['paths']:
        if path.get('scope_reviewed') is not True:
            problems.append(f"{path['id']}: scope not reviewed")
        if path.get('capacity_and_readiness_reviewed') is not True:
            problems.append(f"{path['id']}: capacity/readiness not reviewed")
        layers=[]
        if not path.get('permissions'):
            problems.append(f"{path['id']}: no permission evidence")
        for layer in path.get('permissions',[]):
            if layer.get('review_status')!='verified' or not layer.get('source'):
                problems.append(f"{path['id']}/{layer['id']}: unverified evidence")
            if layer.get('windows') is None:
                problems.append(f"{path['id']}/{layer['id']}: unknown validity")
            else:
                layers.append([Window(*w) for w in layer['windows']])
        paths.append(layers)
    if problems:
        return {'status':'unresolved','reasons':problems,
                'note':'No continuity coverage claim is computed from unresolved prerequisites.'}
    if spec.get('switching',False) and spec.get('handoff_reviewed') is not True:
        return {'status':'unresolved','reasons':['Switching requested without reviewed handoff evidence']}
    result=audit(paths,spec['recovery_days'],Window(*spec['candidate_horizon']),spec.get('switching',False))
    return {'status':'conditional',**result,
            'note':'Coverage follows from supplied reviewed inputs; this is not legal or operational certification.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('portfolio',type=Path)
    args=parser.parse_args(); print(json.dumps(check(json.loads(args.portfolio.read_text())),indent=2))
