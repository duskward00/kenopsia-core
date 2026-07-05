# Changelog

## v0.2.1 - 2026-07-04

### Fixed

- Made the SSH security collector tolerant of unreadable `/etc/ssh/sshd_config`.
- Collector now reports SSH config permission status instead of aborting the full assessment run.
- Added regression coverage for permission-denied SSH config reads.

## v0.2.0 - 2026-07-04

### Added

- Assessment engine foundation.
- Storage collector.
- Security posture collector.
- JSON, Markdown, and HTML assessment outputs.
- v0.2.0 documentation and validation scripts.
