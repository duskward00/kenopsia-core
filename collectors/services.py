from __future__ import annotations
from kenopsia.utils import run

KNOWN_PORTS={22:'SSH',53:'DNS resolver',631:'CUPS printing',1716:'KDE Connect',3389:'Remote Desktop/KRDP',5353:'mDNS/Avahi',5355:'LLMNR',9090:'Cockpit',27036:'Steam Remote Play'}
MGMT={22,3389,5900,5901,9090, cockpit:=9090}

def summarize_ports(raw:str):
    out=[]
    for line in raw.splitlines()[1:]:
        parts=line.split()
        if len(parts)<5: continue
        proto=parts[0]; local=parts[4]
        if ':' not in local: continue
        port_s=local.rsplit(':',1)[-1]
        if not port_s.isdigit(): continue
        port=int(port_s)
        exposure='local' if any(x in local for x in ['127.0.0.1','127.0.0.53','127.0.0.54','[::1]']) else 'network'
        risk='medium' if exposure=='network' and port in {3389,5900,5901} else 'info' if exposure=='network' and port in {9090} else 'low'
        out.append({'service':KNOWN_PORTS.get(port,'Unknown'),'proto':proto,'local':local,'port':port,'exposure':exposure,'risk':risk})
    return out[:60]

def collect() -> dict:
    running=run(['systemctl','list-units','--type=service','--state=running','--no-legend','--no-pager'], timeout=15).splitlines()
    failed=run(['systemctl','--failed','--no-legend','--no-pager'], timeout=15).splitlines()
    timers=run(['systemctl','list-timers','--all','--no-legend','--no-pager'], timeout=15).splitlines()
    raw=run(['ss','-tulpen'], timeout=15)
    ports=summarize_ports(raw)
    findings=[]
    mgmt=[p for p in ports if p['risk']=='medium']
    if failed:
        findings.append({'severity':'medium','title':f'{len(failed)} failed systemd unit(s)','detail':'One or more systemd units are failed.','action':'Run systemctl --failed to investigate.'})
    if mgmt:
        findings.append({'severity':'medium','title':f'{len(mgmt)} remotely reachable management-style port(s)','detail':', '.join([f"{p['service']}:{p['port']}" for p in mgmt]),'action':'Confirm these services are intended and protected by firewall policy.'})
    return {'id':'services','title':'Services','category':'Runtime','health':100 if not findings else 88,'status':'Healthy' if not findings else 'Warning','summary':f'{len(running)} running services, {len(failed)} failed, {len(ports)} listening sockets summarized','findings':findings,'recommendations':[], 'positive':['No failed services' if not failed else '', f'{len(running)} running services', f'{len(timers)} active timers'], 'data':{'running_count':len(running),'failed_count':len(failed),'timer_count':len(timers),'failed_units':'\n'.join(failed),'ports':ports,'raw_ports':raw,'critical':{svc:run(['systemctl','is-active',svc], timeout=5) for svc in ['NetworkManager.service','firewalld.service','sshd.service','cockpit.socket','systemd-resolved.service']}}}
