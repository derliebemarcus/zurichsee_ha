# Changelog

## 0.1.9

### Patch Changes

- 867f043: Use Jenkins and Changesets for integration releases.

All notable changes to this project will be documented in this file.

## [0.1.8](https://github.com/derliebemarcus/homeassistant_zurichsee/compare/v0.1.7...v0.1.8) (2026-06-30)

### Bug Fixes

- **ci:** quote release label condition ([9e0d4a5](https://github.com/derliebemarcus/homeassistant_zurichsee/commit/9e0d4a5e2d16fe7cc20608ed9bd7a804afb30157))
- **release:** accept automated changelog format ([e7b1d2e](https://github.com/derliebemarcus/homeassistant_zurichsee/commit/e7b1d2e27bc6fab46e187e0bcf5dd0d6bce38d68))
- **release:** extract automated changelog entries ([650e0b4](https://github.com/derliebemarcus/homeassistant_zurichsee/commit/650e0b46383b7a612768621c085f627e34b80224))

## [0.1.7] - 2026-06-25

### Added

- Added Switzerland as the integration country in the HACS manifest.

### Changed

- Updated HACS metadata for submission to the default repository.

### Fixed

- Added the country metadata required for geographically limited HACS integrations.

## [0.1.6] - 2026-06-24

### Added

- No new features.

### Changed

- Updated repository, badge, documentation, issue-tracker, and installation links after the repository rename.

### Fixed

- Corrected outdated references to the former repository name.

## [0.1.5] - 2026-06-24

### Changed

- Prepared a stable release for submission to the default HACS store.
- Enabled complete HACS validation without ignored checks.

### Fixed

- Corrected the integration brand image files to use actual PNG encoding.

## [0.1.4] - 2026-04-29

### Added

- Increased test coverage to 99.57%.
- Added comprehensive unit and integration tests.

### Fixed

- Resolved SonarQube issues (unused parameters and unnecessary async).
- Cleaned up unused imports and improved code quality.

## [0.1.3] - 2026-04-29

### Added

- New images

### Changed

### Fixed

## [0.1.1] - 2026-04-29

### Added

- Maintenance scripts

### Fixed

- Resolved dependency conflict between security-mandated pytest 9.0.3 and testing plugin.
- Fixed Error 500 during integration setup by loosening core dependency pins.
- Stabilized CI/CD pipeline with formal constraints strategy.

## [0.1.0] - 2026-04-29

### Added

- Initial release.
- Support for Mythenquai and Tiefenbrunnen stations.
- 15 sensors for each station.
- German and English translations.
- Configuration via UI (Config Flow & Options Flow).
