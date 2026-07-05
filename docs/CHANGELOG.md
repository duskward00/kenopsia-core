# Changelog

## v0.2.2 Sprint 1 / Milestone 2

### Added

- New `kenopsia.assessment` package
- Normalized inventory model
- Finding model with severity weighting
- Recommendation model
- Rule registry
- Assessment engine
- Category scoring
- Initial storage rules
- Initial security rules
- Tests for assessment framework behavior

### Fixed by Design

- Storage assessment now ignores `efivarfs`, preventing false positives on `/sys/firmware/efi/efivars`.

### Notes

This milestone adds the future assessment framework beside the current v0.1.0 runtime. Integration into the main CLI and report pipeline will occur in later milestones.
