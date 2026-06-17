# Slicer Extensions Index submission

This folder holds the **catalog entry** that lists *SlicerForge* in the
[Slicer Extensions Index](https://github.com/Slicer/ExtensionsIndex), so the
extension becomes installable from inside 3D Slicer via **Extensions Manager**.

[`SlicerForge.json`](SlicerForge.json) is the ready-to-submit entry, validated
against Slicer's official
[catalog-entry schema v1.0.1](https://raw.githubusercontent.com/Slicer/Slicer/main/Schemas/slicer-extension-catalog-entry-schema-v1.0.1.json).

## What the entry says

| Field | Value | Why |
|---|---|---|
| `category` | `Informatics` | Matches `EXTENSION_CATEGORY` in the top-level `CMakeLists.txt`. |
| `scm_url` | `https://github.com/DaCameraGirl/slicer-forge.git` | Public, read-only clone URL. |
| `scm_revision` | `main` | The index builds from the tip of `main`. |
| `build_subdirectory` | `.` | Simple (non-superbuild) extension — builds at the repo root. |
| `build_dependencies` | `[]` | No *Slicer extension* build deps. The `dicom-anvil` engine is a **runtime** pip dependency installed by the module, not a build dependency. |
| `tier` | `1` | Experimental — the correct starting tier for a brand-new extension (1 = experimental, 3 = community-supported, 5 = core-supported). |

> The filename **must** match the extension's CMake `project()` name — here
> `project(SlicerForge)` — so it is `SlicerForge.json`.

## Submission steps (the final, outward step is held)

> ⚠️ **Not yet submitted.** Opening the PR below is a public contribution to a
> third-party repository under the maintainer's name, so it is held pending an
> explicit go-ahead. Everything up to that point is prepared here.

When ready:

1. Fork [`Slicer/ExtensionsIndex`](https://github.com/Slicer/ExtensionsIndex).
2. Copy [`SlicerForge.json`](SlicerForge.json) to the **root** of the fork.
   - Target the `main` branch for the Slicer **Preview** release; target the
     version branch (e.g. `5.8`) for the current **Stable** release.
3. Open a PR using the index's PR template and complete its checklist.
4. Watch the Slicer extension build **dashboard** after the first submission and
   after any change, to confirm SlicerForge builds cleanly on Slicer's CI.

## Pre-submission checklist (Slicer's requirements)

- [x] Extension built with the Extension Wizard layout and CMake metadata
      (`EXTENSION_*` in `CMakeLists.txt`).
- [x] Builds and self-tests pass in CI, including a **headless 3D Slicer**
      end-to-end run (see `.github/workflows/slicer-selftest.yml`).
- [x] Read-only `scm_url` resolves and the repo is public.
- [x] Catalog entry validates against the v1.0.1 schema.
- [ ] **Screenshots** added (`EXTENSION_SCREENSHOTURLS` is currently empty) — best
      captured live with Slicer open; see [`../docs/tutorial.md`](../docs/tutorial.md).
- [ ] Plans announced on the [Slicer forum](https://discourse.slicer.org) for
      community feedback (courtesy step before submitting).
- [ ] Upstream PR opened (**held for go-ahead**).

## References

- Slicer developer guide — [Extensions](https://slicer.readthedocs.io/en/latest/developer_guide/extensions.html)
- [Extensions Index repository](https://github.com/Slicer/ExtensionsIndex)
- [Catalog entry schema v1.0.1](https://raw.githubusercontent.com/Slicer/Slicer/main/Schemas/slicer-extension-catalog-entry-schema-v1.0.1.json)
