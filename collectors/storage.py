from __future__ import annotations
import psutil
from kenopsia.utils import gb, run


def lsblk_json():
    import json
    raw=run(['lsblk','-J','-o','NAME,PATH,TYPE,SIZE,MODEL,SERIAL,TRAN,ROTA,FSTYPE,MOUNTPOINTS'], timeout=10)
    try: return json.loads(raw).get('blockdevices',[])
    except Exception: return []

def smart_for(path):
    raw=run(['sudo','smartctl','-H','-A',path], timeout=20)
    lower=raw.lower()
    status='PASSED' if 'passed' in raw or 'self-assessment test result: PASSED' in raw else 'unknown'
    temp=None
    for line in raw.splitlines():
        if 'Temperature:' in line and 'Celsius' in line:
            import re
            m=re.search(r'(\d+)\s+Celsius', line); temp=m.group(1) if m else None
        elif 'Temperature_Celsius' in line or 'Airflow_Temperature' in line:
            vals=line.split(); temp=vals[-1] if vals else temp
    return {'device':path,'status':status,'temperature':temp,'raw':'\n'.join(raw.splitlines()[:45])}

def collect() -> dict:
    volumes=[]; findings=[]; recs=[]
    for p in psutil.disk_partitions(all=False):
        if 'snap' in p.mountpoint or p.fstype=='squashfs': continue
        try: u=psutil.disk_usage(p.mountpoint)
        except Exception: continue
        volumes.append({'device':p.device,'mount':p.mountpoint,'type':p.fstype,'total_gb':gb(u.total),'used_gb':gb(u.used),'free_gb':gb(u.free),'used_percent':u.percent})
        if u.percent >= 90:
            findings.append({'severity':'high','title':f'{p.mountpoint} is critically full','detail':f'{u.percent}% used','action':'Free disk space or expand the filesystem.'})
        elif u.percent >= 80:
            findings.append({'severity':'medium','title':f'{p.mountpoint} is getting full','detail':f'{u.percent}% used','action':'Review large files and retention.'})
    disks=[d for d in lsblk_json() if d.get('type')=='disk']
    smart=[]
    for d in disks:
        path=d.get('path')
        if path and not path.startswith('/dev/zram'):
            smart.append(smart_for(path))
    health=100 if not findings and all(s.get('status')!='FAILED' for s in smart) else 80
    trim=run(['systemctl','is-enabled','fstrim.timer'], timeout=5)
    positives=[]
    if trim=='enabled': positives.append('fstrim.timer is enabled')
    if smart: positives.append('SMART collector ran without failed disk status')
    return {'id':'storage','title':'Storage','category':'Storage','health':health,'status':'Healthy' if health>=90 else 'Warning','summary':f'{len(disks)} disk(s), {len(volumes)} mounted volume(s)','findings':findings,'recommendations':recs,'positive':positives,'data':{'volumes':volumes,'disks':disks,'smart':smart,'trim':trim,'btrfs':run(['btrfs','filesystem','show'], timeout=10),'btrfs_subvolumes':run(['btrfs','subvolume','list','/'], timeout=10)}}
