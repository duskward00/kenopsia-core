from __future__ import annotations
import psutil, cpuinfo
from kenopsia.utils import read, run


def collect() -> dict:
    info = cpuinfo.get_cpu_info() or {}
    cpu = info.get("brand_raw") or "Unknown CPU"
    vendor = read('/sys/class/dmi/id/sys_vendor')
    product = read('/sys/class/dmi/id/product_name')
    board_vendor = read('/sys/class/dmi/id/board_vendor')
    board_name = read('/sys/class/dmi/id/board_name')
    bios_vendor = read('/sys/class/dmi/id/bios_vendor')
    bios_ver = read('/sys/class/dmi/id/bios_version')
    bios_date = read('/sys/class/dmi/id/bios_date')
    lspci = run(["lspci"], timeout=10)
    lsusb = run(["lsusb"], timeout=10)
    gpus = "\n".join([l for l in lspci.splitlines() if any(x in l.lower() for x in ["vga", "3d controller", "display"])] )
    pci_count = len([x for x in lspci.splitlines() if x.strip()])
    usb_lines = [x for x in lsusb.splitlines() if x.strip()]
    return {"id":"hardware","title":"Hardware","category":"Hardware","health":95,"status":"Healthy","summary":cpu,"findings":[],"recommendations":[],"positive":[cpu, f"{pci_count} PCI devices detected", f"{len(usb_lines)} USB devices detected"],"data":{"system":f"{vendor} {product}","motherboard":f"{board_vendor} {board_name}","bios":f"{bios_vendor} {bios_ver} {bios_date}","cpu":cpu,"cores":psutil.cpu_count(logical=False),"threads":psutil.cpu_count(logical=True),"frequency":psutil.cpu_freq().current if psutil.cpu_freq() else None,"frequency_max":psutil.cpu_freq().max if psutil.cpu_freq() else None,"virtualization":"Intel VT-x" if "vmx" in info.get('flags', []) else "AMD-V" if "svm" in info.get('flags', []) else "unknown","gpu":gpus,"pci_count":pci_count,"usb_count":len(usb_lines),"usb_sample":"\n".join(usb_lines[:12])}}
