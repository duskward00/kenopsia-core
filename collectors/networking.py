from __future__ import annotations
import psutil, socket
from kenopsia.utils import run

FAM = {socket.AF_INET:"IPv4", socket.AF_INET6:"IPv6", psutil.AF_LINK:"MAC"}


def collect() -> dict:
    stats = psutil.net_if_stats(); addrs = psutil.net_if_addrs()
    interfaces=[]; active=0
    for name, stat in stats.items():
        rows=[]
        for a in addrs.get(name, []): rows.append({"family":FAM.get(a.family, str(a.family)),"address":a.address,"netmask":a.netmask})
        if stat.isup: active += 1
        interfaces.append({"name":name,"is_up":stat.isup,"speed":stat.speed,"mtu":stat.mtu,"is_bridge":name.startswith('br'),"addresses":rows})
    return {"id":"network","title":"Network","category":"Connectivity","health":100 if active else 60,"status":"Healthy" if active else "Warning","summary":f"{active} active interface(s)","findings":[],"recommendations":[],"positive":[f"{active} active network interface(s)"],"data":{"interfaces":interfaces,"default_route":run(["ip","route","show","default"], timeout=5),"dns":run(["resolvectl","dns"], timeout=5)}}
