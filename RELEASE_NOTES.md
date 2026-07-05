# Kenopsia Core v0.2.1 Release Notes

Maintenance release for the v0.2.x assessment foundation.

## Fixed

- Security collector no longer crashes when `/etc/ssh/sshd_config` exists but is not readable by the current user.
- SSH configuration collection now records `permission_denied` and allows the assessment/report pipeline to continue.

## Validation

- Compile check
- Pytest suite
- CLI version check
- Local assessment/report generation
