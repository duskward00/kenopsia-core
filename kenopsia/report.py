from __future__ import annotations
import json, shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


def render(data: dict, outdir: str = 'reports') -> tuple[Path, Path]:
    out=Path(outdir); out.mkdir(exist_ok=True)
    html=out/'kenopsia-report.html'; jsn=out/'kenopsia-report.json'
    jsn.write_text(json.dumps(data, indent=2), encoding='utf-8')
    env=Environment(loader=FileSystemLoader('templates'), autoescape=select_autoescape(['html','xml']))
    tmpl=env.get_template('report.html')
    html.write_text(tmpl.render(report=data), encoding='utf-8')
    hist=Path('history'); hist.mkdir(exist_ok=True)
    stamp=data.get('generated_at','scan').replace(':','').replace(' ','-')
    shutil.copy2(jsn, hist/f'{stamp}.json')
    return html, jsn
