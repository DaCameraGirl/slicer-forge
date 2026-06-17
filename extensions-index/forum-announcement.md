# Slicer forum announcement (draft)

A ready-to-post draft for the [3D Slicer forum](https://discourse.slicer.org)
(category: **Development**). Slicer asks new extension authors to announce their
plans before submitting to the Extensions Index, so the community can give
feedback. Edit to taste, then post. It is your voice, so make it yours.

---

**Title:** New extension: SlicerForge (DICOM Forge Batch), batch de-identify, QC and import of DICOM

**Body:**

Hi all,

I'd like to introduce a new extension I'm preparing to submit to the Extensions
Index: **SlicerForge**, which adds a module called **DICOM Forge Batch**
(Informatics category).

It batch-imports DICOM into Slicer by running each series through a headless
pipeline: **ingest, de-identify, quality-control, convert (NRRD/NIfTI), and load
into the scene**. The goal is to turn a folder of messy clinical DICOM into
clean, de-identified, QC'd volumes ready for research in one pass, with an
audit record per series.

A few design notes that may interest this community:

- The heavy lifting lives in a **separate, headless engine** (`dicom-anvil` on
  PyPI, imported as `dicomforge`), so the logic is unit-tested without Slicer and
  the Slicer module stays a thin GUI. It is the same kind of engine and GUI split
  that Slicer itself uses with ITK and VTK.
- CI runs the **full pipeline in a real headless Slicer** on every push, plus the
  engine's own test matrix.
- It's **open-core**: the Slicer extension is Apache-2.0, and the engine is
  PolyForm Noncommercial (free for research and education).

Repo: https://github.com/DaCameraGirl/slicer-forge
Engine: https://github.com/DaCameraGirl/dicom-forge and https://pypi.org/project/dicom-anvil/

I'd welcome any feedback before I open the ExtensionsIndex PR, especially on the
de-identification profiles and anything you'd expect from a batch DICOM importer.

Thanks!
Angela

---

After posting, link this thread in the ExtensionsIndex PR description, and tick
the forum-announcement box in [`README.md`](README.md).
