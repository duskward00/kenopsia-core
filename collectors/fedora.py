from __future__ import annotations
from kenopsia.utils import run


def count_lines(text): return len([x for x in text.splitlines() if x.strip()])

def collect() -> dict:
    rpm_count=count_lines(run(['rpm','-qa'], timeout=20))
    flatpak_raw=run(['flatpak','list','--app'], timeout=20)
    flatpak_count=0 if flatpak_raw.startswith('Unavailable') else count_lines(flatpak_raw)
    updates_raw=run(['dnf','check-update'], timeout=60)
    update_lines=[l for l in updates_raw.splitlines() if l.strip() and not l.startswith(('Last metadata','Upgrades')) and ('.x86_64' in l or '.noarch' in l or '.i686' in l)]
    updates=len(update_lines)
    extras=run(['dnf','repoquery','--extras'], timeout=30)
    dupes=run(['dnf','repoquery','--duplicates'], timeout=30)
    findings=[]; recs=[]; health=100
    if updates > 100:
        health=80; findings.append({'severity':'medium','title':f'{updates} pending package updates','detail':'A larger update backlog may include security and stability fixes.','action':'Run sudo dnf upgrade when ready.'})
        recs.append({'severity':'medium','title':'Apply pending Fedora updates','detail':f'{updates} package updates are available.','action':'sudo dnf upgrade'})
    elif updates > 0:
        health=90
    return {'id':'fedora','title':'Fedora','category':'Maintenance','health':health,'status':'Healthy' if health>=90 else 'Warning','summary':f'{rpm_count} RPM packages, {updates} pending update(s)','findings':findings,'recommendations':recs,'positive':[f'{rpm_count} RPM packages inventoried', f'{flatpak_count} Flatpak apps inventoried'], 'data':{'rpm_count':rpm_count,'flatpak_count':flatpak_count,'pending_updates':updates,'pending_sample':'\n'.join(update_lines[:80]),'kernels':run(['rpm','-q','kernel-core'], timeout=10),'repos':run(['dnf','repolist','--enabled'], timeout=20),'history':run(['dnf','history','list'], timeout=20),'extras':extras,'duplicates':dupes}}
