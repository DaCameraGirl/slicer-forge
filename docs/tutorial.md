# Tutorial: batch-importing DICOM with DICOM Forge Batch

This walks through a complete run of the **DICOM Forge Batch** module — from a
folder of raw DICOM to de-identified, quality-controlled volumes loaded into
your 3D Slicer scene. It assumes you have 3D Slicer installed; see the
[README](../README.md) for how to add the module.

> ⚠️ De-identification is best-effort risk reduction, **not** a compliance
> guarantee. You are responsible for validating that output meets your
> jurisdiction's and institution's disclosure rules before any data leaves a
> controlled environment.

<!-- screenshot: the DICOM Forge Batch module panel, full height -->

## 1. Open the module

In Slicer, use the module selector (the magnifier, or `Ctrl+F`) and search for
**DICOM Forge Batch**. It lives under the **Informatics** category. The panel
has four sections: *Dependencies*, *Input / Output*, *Options*, and the run
controls.

## 2. Install the engine (first run only)

The module is a thin GUI; the real work is done by the
[`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge) pipeline, which
runs inside Slicer's own Python. The *Dependencies* section shows whether it is
present.

- If it says **not installed**, click **Install / update dicom-forge**. This
  runs `pip_install` into Slicer's environment (not your system Python) and
  pulls in the conversion libraries (SimpleITK, pynrrd, nibabel).
- When it shows **installed ✓**, you are ready. You only need to do this once
  per Slicer installation.

<!-- screenshot: Dependencies section showing "installed ✓" -->

## 3. Pick your folders

In *Input / Output*:

- **DICOM folder** — a folder containing one or more DICOM series. Series are
  detected automatically by their Series Instance UID, so it is fine if several
  series (even different modalities) sit in the same folder.
- **Output folder** — where the converted volumes are written. It is created if
  it does not exist.

The **Run** button stays disabled until both folders are set and the engine is
installed.

## 4. Choose options

- **De-identification** — how aggressively patient-identifying tags are
  removed: `basic`, `moderate` (default), or `strict`.
- **Output format** — `nrrd` (Slicer's native scalar volume format,
  recommended) or `nifti`.
- **Load converted volumes into the scene** — leave checked to have each
  converted volume appear in Slicer immediately; uncheck to only write files.

## 5. Run

Click **Run batch import**. For each series the module:

1. de-identifies it at the level you chose,
2. runs quality control,
3. converts it to your chosen format, and
4. (if enabled) loads it into the scene.

A progress bar advances per series. On a large folder the panel stays
responsive, and you can click **Cancel** at any time — the batch stops cleanly
after the series it is currently working on, and the results so far are kept.

<!-- screenshot: a completed run showing the per-series PASS/FAIL summary -->

## 6. Read the results

The results panel lists one line per series, for example:

```
Processed 2 series:

- CT (120 slices) QC=PASS -> C:/out/series_000.nrrd
- MR (160 slices) QC=PASS -> C:/out/series_001.nrrd
```

`QC=PASS` means no QC errors were found; any warnings are listed indented
beneath the series. Loaded volumes are named `DICOMForge_<modality>_<index>` in
the scene.

## Troubleshooting

- **"No readable DICOM series found"** — the input folder has no DICOM the
  pipeline can read. Check you pointed at the right folder; non-DICOM files are
  ignored.
- **The Run button is greyed out** — make sure the engine shows **installed ✓**
  and both folders are selected.
- **Install fails** — the engine is installed from its public GitHub repository
  until it is published to PyPI, so the machine needs network access. The error
  dialog includes the underlying pip output.
- **A series shows `QC=FAIL`** — QC found a hard error (for example inconsistent
  slice geometry). The volume may still convert, but treat it with caution; the
  warnings/errors explain what was found.

## What's next

This tutorial covers the GUI. The same pipeline is scriptable from the Python
console via `DicomForgeBatchLogic().process(...)`, and headlessly via the
[`dicom-forge` library and CLI](https://dacameragirl.github.io/dicom-forge/).
