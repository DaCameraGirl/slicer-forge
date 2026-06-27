<p align="center">
  <img src="docs/readme-banner.svg" alt="Slicer Forge — 3D Slicer extension: batch ingest, de-identify, QC, and import DICOM via the dicom-forge pipeline." width="720" />
</p>

<p align="center">
  <strong>3D Slicer extension: batch ingest, de-identify, QC, and import DICOM via the dicom-forge pipeline.</strong>
</p>

<p align="center">
  <a href="https://dacameragirl.github.io/slicer-forge/"><img src="https://img.shields.io/badge/Live-GitHub%20Pages-33d69f?style=for-the-badge&logo=github&logoColor=white" alt="Live demo" /></a>
  <a href="https://github.com/DaCameraGirl/slicer-forge"><img src="https://img.shields.io/badge/Code-GitHub-58a6ff?style=for-the-badge&logo=github&logoColor=white" alt="Source code" /></a>
  <a href="https://github.com/DaCameraGirl/dicom-forge"><img src="https://img.shields.io/badge/dicom-forge-33d69f?style=for-the-badge" alt="dicom-forge" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/deploy-GitHub Pages-000000?style=flat-square&logo=github&logoColor=white" alt="deploy-GitHub Pages" />
  <img src="https://img.shields.io/badge/medical-imaging-4fd6e0?style=flat-square" alt="medical-imaging" />
</p>

### Languages

<p align="center">
  <img src="https://img.shields.io/badge/Python-89%25-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/PowerShell-8%25-5391FE?style=flat-square&logo=github&logoColor=white" alt="PowerShell" />
</p>

### Stack

<p align="center">
  <img src="https://img.shields.io/badge/3D Slicer-ext-4fd6e0?style=flat-square" alt="3D Slicer-ext" />
  <img src="https://img.shields.io/badge/dicom-forge-pipeline-33d69f?style=flat-square" alt="dicom-forge-pipeline" />
</p>

<p align="center">
  Built by <strong>Angela Hudson</strong> · <a href="https://github.com/DaCameraGirl">DaCameraGirl</a>
</p>
<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸_English-a78bfa?style=for-the-badge" alt="English"/></a>
    <a href="README.es.md"><img src="https://img.shields.io/badge/🇪🇸_Español-1e293b?style=for-the-badge" alt="Español"/></a>
    <a href="README.fr.md"><img src="https://img.shields.io/badge/🇫🇷_Français-1e293b?style=for-the-badge" alt="Français"/></a>
    <a href="README.de.md"><img src="https://img.shields.io/badge/🇩🇪_Deutsch-1e293b?style=for-the-badge" alt="Deutsch"/></a>
    <a href="README.pt-BR.md"><img src="https://img.shields.io/badge/🇧🇷_Português-1e293b?style=for-the-badge" alt="Português"/></a>
</p>
<p align="center">
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/🇨🇳_中文-1e293b?style=for-the-badge" alt="中文"/></a>
    <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵_日本語-1e293b?style=for-the-badge" alt="日本語"/></a>
    <a href="README.ko.md"><img src="https://img.shields.io/badge/🇰🇷_한국어-1e293b?style=for-the-badge" alt="한국어"/></a>
    <a href="README.it.md"><img src="https://img.shields.io/badge/🇮🇹_Italiano-1e293b?style=for-the-badge" alt="Italiano"/></a>
    <a href="README.ar.md"><img src="https://img.shields.io/badge/🇸🇦_العربية-1e293b?style=for-the-badge" alt="العربية"/></a>
</p>

<p align="center">
  <img src="docs/assets/slicer-batch.svg" alt="Animated Slicer Forge batch pipeline — folders through de-id into 3D volumes" width="520"/>
</p>

<p align="center">
  <img src="docs/assets/deid-scanner.svg" alt="DICOM de-identification — x-ray scan with names redacted from paperwork" width="420"/>
</p>

<p align="center">
  <a href="https://github.com/DaCameraGirl/slicer-forge/actions/workflows/ci.yml"><img src="https://github.com/DaCameraGirl/slicer-forge/actions/workflows/ci.yml/badge.svg" alt="Lint"/></a>
  <img src="https://img.shields.io/badge/license-Apache--2.0-green.svg" alt="License"/>
  <img src="https://img.shields.io/badge/3D%20Slicer-extension-a78bfa.svg" alt="Slicer extension"/>
</p>

**A [3D Slicer](https://www.slicer.org/) extension that batch-imports DICOM through the [`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge) pipeline.**

`slicer-forge` adds a **DICOM Forge Batch** module to Slicer. Point it at a folder of DICOM, and it de-identifies each series (removes patient names and IDs from headers), runs quality control, converts to NRRD, and loads the volumes straight into your Slicer scene — driven entirely by the headless, independently tested `dicom-forge` library.

<p align="center">
  <img src="DicomForgeBatch/Resources/Icons/DicomForgeBatch.png" width="96" alt="DICOM Forge Batch icon">
</p>

<p align="center"><img src="docs/readme-divider.svg" width="720" alt="" /></p>
<p align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:070b14,100:12102a&height=50&section=header&text=The%20two-repo%20design&fontSize=22&fontColor=e6edf3&animation=twinkling" width="720" alt="The two-repo design" /></p>


| Repo | Role | Tested |
|------|------|--------|
| [`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge) | Headless pipeline (ingest · de-id · QC · convert) | Unit-tested in CI without Slicer |
| **`slicer-forge`** (this) | Thin Slicer GUI on top of it | Self-test runs inside Slicer |

This mirrors how Slicer itself is built (ITK/VTK do the work; the GUI is a shell on top). All the heavy logic lives in `dicom-forge`, so it is fully testable on its own; this repo stays a small, focused front-end.

<p align="center"><img src="docs/readme-divider.svg" width="720" alt="" /></p>
<p align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:070b14,100:12102a&height=50&section=header&text=What%20the%20module%20does&fontSize=22&fontColor=e6edf3&animation=twinkling" width="720" alt="What the module does" /></p>


1. **Install dependencies** — one button runs `pip_install('dicom-anvil[convert]')` into Slicer's own Python environment (the engine ships on PyPI as `dicom-anvil`; it still imports as `dicomforge`).
2. **Pick folders** — a DICOM input folder and an output folder.
3. **Choose options** — de-identification level (basic / moderate / strict) and output format (NRRD / NIfTI).
4. **Run** — every series is de-identified → QC'd → converted → loaded into the scene, with a per-series PASS/FAIL summary and warnings. Long runs stay responsive and can be cancelled.

📖 **New to the module?** Follow the step-by-step [usage tutorial](docs/tutorial.md). See the [changelog](CHANGELOG.md) for what has changed.

<p align="center"><img src="docs/readme-divider.svg" width="720" alt="" /></p>
<p align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:070b14,100:12102a&height=50&section=header&text=Installation&fontSize=22&fontColor=e6edf3&animation=twinkling" width="720" alt="Installation" /></p>


### From source (developer install)

```bash
git clone https://github.com/DaCameraGirl/slicer-forge.git
```

In Slicer: **Edit → Application Settings → Modules → Additional module paths**, add the `slicer-forge/DicomForgeBatch` folder, and restart. The **DICOM Forge Batch** module appears under the *Informatics* category.

### Build as a loadable extension

The repo is laid out for the standard Slicer extension build (`CMakeLists.txt` + `slicerMacroBuildScriptedModule`) so it can be built against a Slicer build tree and submitted to the [Slicer Extensions Index](https://github.com/Slicer/ExtensionsIndex).

<p align="center"><img src="docs/readme-divider.svg" width="720" alt="" /></p>
<p align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:070b14,100:12102a&height=50&section=header&text=Module%20anatomy&fontSize=22&fontColor=e6edf3&animation=twinkling" width="720" alt="Module anatomy" /></p>


Slicer scripted modules use a fixed four-class shape — this one lives in [`DicomForgeBatch/DicomForgeBatch.py`](DicomForgeBatch/DicomForgeBatch.py):

- `DicomForgeBatch` — module metadata.
- `DicomForgeBatchWidget` — the GUI panel (built programmatically).
- `DicomForgeBatchLogic` — Qt-free logic wrapping `dicom-forge` (reusable from the Python console).
- `DicomForgeBatchTest` — a self-test that generates synthetic DICOM and runs the whole pipeline inside Slicer.

<p align="center"><img src="docs/readme-divider.svg" width="720" alt="" /></p>
<p align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:070b14,100:12102a&height=50&section=header&text=Testing&fontSize=22&fontColor=e6edf3&animation=twinkling" width="720" alt="Testing" /></p>


The self-test runs **inside** Slicer (it needs the `slicer` runtime):

> Slicer → **Developer Tools → Self Tests** → run *DicomForgeBatch*, or from the Python console: `slicer.util.selfTest('DicomForgeBatch')`.

CI runs on every push at two levels:

- a **fast lane** lint-checks and byte-compiles the module, and
- a **headless-Slicer lane** that downloads real 3D Slicer and runs the full pipeline end-to-end — de-id → QC → convert → load — across CT and MR, multiple series, both output formats, every de-identification level, and failure paths.

> ⚠️ De-identification is best-effort risk reduction, not a compliance guarantee. See [`dicom-forge`'s SECURITY policy](https://github.com/DaCameraGirl/dicom-forge/blob/main/SECURITY.md).

<p align="center"><img src="docs/readme-divider.svg" width="720" alt="" /></p>
<p align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:070b14,100:12102a&height=50&section=header&text=License&fontSize=22&fontColor=e6edf3&animation=twinkling" width="720" alt="License" /></p>


[Apache-2.0](LICENSE) © Angela Hudson