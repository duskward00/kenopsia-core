from __future__ import annotations
from kenopsia.utils import run, read


def systemctl_state(unit): return run(['systemctl','is-active',unit], timeout=5)
def systemctl_enabled(unit): return run(['systemctl','is-enabled',unit], timeout=5)

def ssh_effective():
    raw=run(['sshd','-T'], timeout=10)
    data={}
    for line in raw.splitlines():
        parts=line.split(None,1)
        if len(parts)==2: data[parts[0]]=parts[1]
    return data

def collect() -> dict:
    findings=[]; recs=[]; positives=[]; health=100
    selinux=run(['getenforce'], timeout=5)
    if selinux=='Enforcing': positives.append('SELinux is enforcing')
    else:
        health-=20; findings.append({'severity':'high','title':'SELinux is not enforcing','detail':f'SELinux status: {selinux}','action':'Review SELinux mode and policy.'})
    fw_active=systemctl_state('firewalld.service'); fw_enabled=systemctl_enabled('firewalld.service')
    if fw_active=='active': positives.append('firewalld is active')
    else:
        health-=20; findings.append({'severity':'high','title':'firewalld is not active','detail':'Host firewall is not active.','action':'Enable firewalld if appropriate.'})
    secure=run(['mokutil','--sb-state'], timeout=5); sb='enabled' if 'enabled' in secure.lower() else 'disabled' if 'disabled' in secure.lower() else 'unknown'
    if sb=='disabled':
        health-=8; findings.append({'severity':'low','title':'Secure Boot is disabled','detail':'Boot-chain verification is not active.','action':'Enable Secure Boot if practical and compatible with installed drivers.'})
        recs.append({'severity':'low','title':'Consider enabling Secure Boot','detail':'Secure Boot can improve protection against boot-chain tampering.','action':'Enable Secure Boot in firmware after validating driver compatibility.'})
    tpm='detected' if read('/sys/class/tpm/tpm0/tpm_version_major','') else 'not detected'
    ssh_active=systemctl_state('sshd.service'); ssh_enabled=systemctl_enabled('sshd.service')
    ssh=ssh_effective() if ssh_active=='active' or ssh_enabled=='enabled' else {}
    if ssh.get('passwordauthentication')=='yes':
        health-=10; findings.append({'severity':'medium','title':'SSH password authentication enabled','detail':'Password-based SSH login is enabled.','action':'Consider key-based authentication only.'})
    else: positives.append('SSH password authentication is not enabled')
    auto=systemctl_enabled('dnf-automatic.timer')
    if auto in ['enabled','static','alias']: positives.append('Automatic update timer appears configured')
    else: recs.append({'severity':'low','title':'Consider enabling automatic update checks','detail':'dnf-automatic can keep maintenance visibility current.','action':'sudo dnf install dnf-automatic && sudo systemctl enable --now dnf-automatic.timer'})
    fw_detail=run(['firewall-cmd','--list-all'], timeout=10)
    return {'id':'security','title':'Security','category':'Security','health':max(0,health),'status':'Healthy' if health>=90 else 'Warning','summary':f'SELinux {selinux}, firewall {fw_active}, Secure Boot {sb}','findings':findings,'recommendations':recs,'positive':positives,'data':{'selinux':selinux,'firewalld_active':fw_active,'firewalld_enabled':fw_enabled,'firewall_backend':run(['firewall-cmd','--get-log-denied'], timeout=5),'firewall_default_zone':run(['firewall-cmd','--get-default-zone'], timeout=5),'firewall_detail':fw_detail,'secure_boot':sb,'tpm':tpm,'auto_updates':auto,'ssh':{'installed':not run(['which','sshd'], timeout=5).startswith('Unavailable'),'active':ssh_active,'enabled':ssh_enabled,'port':ssh.get('port','unknown'),'passwordauthentication':ssh.get('passwordauthentication','unknown'),'permitrootlogin':ssh.get('permitrootlogin','unknown'),'pubkeyauthentication':ssh.get('pubkeyauthentication','unknown')},'sudoers':'present' if read('/etc/sudoers','') else 'unknown','wheel':run(['getent','group','wheel'], timeout=5)}}
