"""Regenerate results from public milestone dates and declared stress inputs."""
import csv
import json
from datetime import date
from pathlib import Path
from src.continuity import Window, audit

ROOT = Path(__file__).resolve().parents[1]

def run():
    result_dir=ROOT/'results'; result_dir.mkdir(exist_ok=True)
    milestones = {'kiribati_contract_to_operating_licence_days':
                   (date(2024,12,6)-date(2024,8,1)).days,
                  'ltms_announcement_to_wheeling_signature_days':
                   (date(2026,1,14)-date(2024,9,20)).days}
    (result_dir/'milestones.json').write_text(json.dumps(milestones,indent=2)+'\n')
    # Deliberately hypothetical. 180 and 365 are stress window lengths, not
    # conversions of any named country's six-month or twelve-month licence.
    portfolios = {
      'one_365_day_path':[[[Window(0,365)]]],
      'two_coexpiring_paths':[[[Window(0,365)]],[[Window(0,365)]]],
      'two_staggered_paths':[[[Window(0,365)]],[[Window(180,545)]]],
      '365_day_service_180_day_site':[[[Window(0,365)],[Window(0,180)]]],
      '365_day_path_90_day_continuation':[[[Window(0,455)]]],
    }
    rows=[]
    for name, paths in portfolios.items():
        for r in range(1,181):
            for switching in (False,True):
                a=audit(paths,r,Window(0,365),switching)
                rows.append({'portfolio':name,'duration_days':r,'switching':int(switching),
                             'safe_start_days':a['safe_days'],
                             'uncovered_start_days':365-a['safe_days'],
                             'coverage_fraction':a['safe_days']/365})
    with (result_dir/'stress_grid.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    headline=[r for r in rows if r['duration_days']==90]
    (result_dir/'headline.json').write_text(json.dumps(headline,indent=2)+'\n')
    print(json.dumps({'milestones':milestones,'stress_rows':len(rows),'at_90_days':headline},indent=2))

if __name__=='__main__':run()
