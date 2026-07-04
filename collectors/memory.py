from __future__ import annotations
import psutil
from kenopsia.utils import gb, run


def collect() -> dict:
    m = psutil.virtual_memory(); s = psutil.swap_memory()
    health = 100 if m.percent < 85 else 75
    findings=[]; recs=[]
    if m.percent >= 85:
        findings.append({"severity":"medium","title":"High memory utilization","detail":f"Memory is {m.percent}% used.","action":"Review running applications and services."})
    dimm = run(["sudo", "dmidecode", "-t", "memory"], timeout=15)
    return {"id":"memory","title":"Memory","category":"Hardware","health":health,"status":"Healthy" if health>=90 else "Warning","summary":f"{gb(m.total)} GB installed, {m.percent}% used","findings":findings,"recommendations":recs,"positive":[f"{gb(m.total)} GB installed"],"data":{"total_gb":gb(m.total),"used_gb":gb(m.used),"available_gb":gb(m.available),"used_percent":m.percent,"swap_total_gb":gb(s.total),"swap_used_percent":s.percent,"dimm_sample":"\n".join(dimm.splitlines()[:80])}}
