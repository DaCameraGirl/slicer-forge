# slicer-forge

[![Lint](https://github.com/DaCameraGirl/slicer-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/DaCameraGirl/slicer-forge/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![Slicer extension](https://img.shields.io/badge/3D%20Slicer-extension-blue.svg)](https://www.slicer.org/)

**A [3D Slicer](https://www.slicer.org/) extension that batch-imports DICOM through the [`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge) pipeline.**

`slicer-forge` adds a **DICOM Forge Batch** module to Slicer. Point it at a folder of
DICOM, and it de-identifies each series, runs quality control, converts to NRRD, and
loads the volumes straight into your Slicer scene — driven entirely by the headless,
independently tested `dicom-forge` library.

<p align="center">
  <img src="DicomForgeBatch/Resources/Icons/DicomForgeBatch.png" width="96" alt="DICOM Forge Batch icon">
</p>

## The two-repo design

| Repo | Role | Tested |
|------|------|--------|
| [`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge) | Headless pipeline (ingest · de-id · QC · convert) | Unit-tested in CI without Slicer |
| **`slicer-forge`** (this) | Thin Slicer GUI on top of it | Self-test runs inside Slicer |

This mirrors how Slicer itself is built (ITK/VTK do the work; the GUI is a shell on
top). All the heavy logic lives in `dicom-forge`, so it is fully testable on its own;
this repo stays a small, focused front-end.

## What the module does

1. **Install dependencies** — one button runs `pip_install('dicom-forge[convert]')`
   into Slicer's own Python environment.
2. **Pick folders** — a DICOM input folder and an output folder.
3. **Choose options** — de-identification level (basic / moderate / strict) and output
   format (NRRD / NIfTI).
4. **Run** — every series is de-identified → QC'd → converted → loaded into the scene,
   with a per-series PASS/FAIL summary and warnings.

## Installation

### From source (developer install)

```bash
git clone https://github.com/DaCameraGirl/slicer-forge.git
```

In Slicer: **Edit → Application Settings → Modules → Additional module paths**, add the
`slicer-forge/DicomForgeBatch` folder, and restart. The **DICOM Forge Batch** module
appears under the *Informatics* category.

### Build as a loadable extension

The repo is laid out for the standard Slicer extension build (`CMakeLists.txt` +
`slicerMacroBuildScriptedModule`) so it can be built against a Slicer build tree and
submitted to the [Slicer Extensions Index](https://github.com/Slicer/ExtensionsIndex).

## Module anatomy

Slicer scripted modules use a fixed four-class shape — this one lives in
[`DicomForgeBatch/DicomForgeBatch.py`](DicomForgeBatch/DicomForgeBatch.py):

- `DicomForgeBatch` — module metadata.
- `DicomForgeBatchWidget` — the GUI panel (built programmatically).
- `DicomForgeBatchLogic` — Qt-free logic wrapping `dicom-forge` (reusable from the
  Python console).
- `DicomForgeBatchTest` — a self-test that generates synthetic DICOM and runs the
  whole pipeline inside Slicer.

## Testing

The self-test runs **inside** Slicer (it needs the `slicer` runtime):

> Slicer → **Developer Tools → Self Tests** → run *DicomForgeBatch*, or from the
> Python console: `slicer.util.selfTest('DicomForgeBatch')`.

CI in this repo lint-checks and byte-compiles the module Python on every push
(the GUI/runtime parts can only execute inside Slicer).

> ⚠️ De-identification is best-effort risk reduction, not a compliance guarantee.
> See [`dicom-forge`'s SECURITY policy](https://github.com/DaCameraGirl/dicom-forge/blob/main/SECURITY.md).

## License

[Apache-2.0](LICENSE) © Angela Hudson
