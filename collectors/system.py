from __future__ import annotations
from datetime import datetime
import platform, socket, psutil, distro
from kenopsia.utils import run


def collect() -> dict:
    boot = datetime.fromtimestamp(psutil.boot_time())
    secure = run(["mokutil", "--sb-state"], timeout=5)
    sb = "enabled" if "enabled" in secure.lower() else "disabled" if "disabled" in secure.lower() else "unknown"
    finding = []
    recs = []
    health = 100
    if sb == "disabled":
        health -= 10
        finding.append({"severity":"low","title":"Secure Boot is disabled","detail":"Boot-chain verification is not active.","action":"Enable Secure Boot if compatible with your firmware and drivers."})
        recs.append({"severity":"low","title":"Consider enabling Secure Boot","detail":"Secure Boot can improve protection against boot-chain tampering.","action":"Enable Secure Boot in firmware after validating driver compatibility."})
    return {"id":"system","title":"System","category":"Core","health":health,"status":"Healthy" if health>=90 else "Warning","summary":f"{distro.name(pretty=True)} on kernel {platform.release()}","findings":finding,"recommendations":recs,"positive":[f"{distro.name(pretty=True)} on kernel {platform.release()}"],"data":{"hostname":socket.gethostname(),"fqdn":socket.getfqdn(),"os":distro.name(pretty=True),"kernel":platform.release(),"architecture":platform.machine(),"boot_time":boot.strftime('%Y-%m-%d %H:%M:%S'),"uptime":str(datetime.now()-boot).split('.')[0],"virtualization":run(["systemd-detect-virt"], timeout=5) or "none","secure_boot":sb}}
