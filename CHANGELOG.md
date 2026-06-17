# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); the project will adopt
[Semantic Versioning](https://semver.org/) at its first tagged release.

## [Unreleased]

### Changed
- Dependency install now pins the engine to its **PyPI release**
  (`dicom-anvil[convert]>=0.1.0`) instead of `git+https://...@main`, so installs
  are reproducible and need no build toolchain (#18).

### Added
- Initial **DICOM Forge Batch** Slicer module (Informatics category): batch
  de-identify → QC → convert → load, driven by the `dicom-forge` pipeline, with
  a one-click dependency installer and a synthetic-DICOM self-test (#2).
- **Cancel** button and a cancellable, responsive batch loop. Scene loading
  stays on the main thread (required for MRML safety); the logic accepts a
  Qt-free `should_cancel()` callable so it remains headless-testable (#7).
- **Headless-Slicer CI**: the full pipeline runs in a real, headless 3D Slicer
  on every push, not just lint/compile (#9).
- Broadened end-to-end self-test to seven labelled checks — CT and MR,
  multi-series in one folder, NRRD and NIfTI output, all de-identification
  levels, and the empty-folder / non-DICOM failure paths (#11).
- Step-by-step usage [tutorial](docs/tutorial.md) and this changelog (#13).

### Fixed
- Results panel no longer raises a `KeyError` after a successful run when a
  result record is missing or has a changed shape; fields are read with
  fallbacks (#5).
- Dependency install used a PEP 508 `name @ url` spec containing spaces, which
  `slicer.util.pip_install` split into invalid pip arguments — the "Install
  dicom-forge" button never worked for the git path. Switched to the no-space
  `name[extras]@url` form (surfaced by the headless-Slicer CI).
- Synthetic-data helper falls back across pydicom versions
  (`enforce_file_format` vs `write_like_original`) so it works whichever
  generation Slicer bundles (#3).
