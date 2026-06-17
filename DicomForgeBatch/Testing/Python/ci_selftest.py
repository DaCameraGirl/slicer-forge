"""Headless end-to-end self-test for CI.

Runs inside a real (headless) 3D Slicer:

    xvfb-run Slicer --no-splash --no-main-window --python-script ci_selftest.py

Adapted from ``scratch/run_live_test.py`` (which passed against Slicer 5.10).
It installs dicom-forge into Slicer's own Python via the module's own
``ensure_dependencies()`` -- so CI exercises the exact install path users hit --
then runs a battery of labelled checks over the pipeline: single CT series,
CT+MR multi-series in one folder, NIfTI output, every de-identification level,
the cancellation path, and the empty/junk-folder failure paths.

The Slicer launcher does not reliably propagate stdout or the process exit code
on every platform, so the verdict is also written to ``CI_RESULT_FILE`` (or a
sibling ``ci_result.txt``). The workflow greps that file for ``EXIT_STATUS=0``.
"""

import os
import sys
import tempfile
import traceback

import slicer

HERE = os.path.dirname(os.path.abspath(__file__))
MODULE_DIR = os.path.normpath(os.path.join(HERE, "..", ".."))  # .../DicomForgeBatch
TESTDATA_DIR = HERE
RESULT_FILE = os.environ.get("CI_RESULT_FILE", os.path.join(HERE, "ci_result.txt"))

for _p in (MODULE_DIR, TESTDATA_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

_log = []


def log(msg):
    print(msg, flush=True)
    _log.append(str(msg))


def _volume_count():
    return len(slicer.util.getNodesByClass("vtkMRMLScalarVolumeNode"))


def _fresh_io():
    tmp = tempfile.mkdtemp()
    return os.path.join(tmp, "in"), os.path.join(tmp, "out")


# --- checks ------------------------------------------------------------------
# Each check raises on failure; the runner clears the scene before each one.
_CHECKS = []


def check(name):
    def _register(fn):
        _CHECKS.append((name, fn))
        return fn

    return _register


def _run_checks(logic):
    from dicomforge_testdata import write_multiple_series, write_synthetic_series

    @check("single CT series -> NRRD, loaded into scene")
    def _():
        in_dir, out_dir = _fresh_io()
        write_synthetic_series(in_dir, num_slices=6, modality="CT")
        results = logic.process(in_dir, out_dir, output_format="nrrd", load_into_scene=True)
        assert len(results) == 1, f"expected 1 series, got {len(results)}"
        assert results[0]["qc"]["geometry_consistent"], results[0]["qc"]
        assert _volume_count() == 1, f"expected 1 volume node, got {_volume_count()}"

    @check("CT + MR multi-series in one folder -> two volumes")
    def _():
        in_dir, out_dir = _fresh_io()
        write_multiple_series(in_dir, modalities=["CT", "MR"], num_slices=4)
        results = logic.process(in_dir, out_dir, load_into_scene=True)
        assert len(results) == 2, f"expected 2 series, got {len(results)}"
        modalities = sorted(r["metadata"]["modality"] for r in results)
        assert modalities == ["CT", "MR"], modalities
        assert _volume_count() == 2, f"expected 2 volume nodes, got {_volume_count()}"

    @check("NIfTI output format")
    def _():
        in_dir, out_dir = _fresh_io()
        write_synthetic_series(in_dir, num_slices=4, modality="CT")
        results = logic.process(in_dir, out_dir, output_format="nifti", load_into_scene=True)
        assert len(results) == 1, f"expected 1 series, got {len(results)}"
        out_path = results[0]["conversion"]["output_path"]
        assert os.path.exists(out_path), f"converted file missing: {out_path}"
        assert _volume_count() == 1, f"expected 1 volume node, got {_volume_count()}"

    @check("de-identification levels: basic / moderate / strict")
    def _():
        for level in ("basic", "moderate", "strict"):
            in_dir, out_dir = _fresh_io()
            write_synthetic_series(in_dir, num_slices=3, modality="CT")
            results = logic.process(in_dir, out_dir, deid_level=level, load_into_scene=False)
            assert len(results) == 1, f"{level}: expected 1 series, got {len(results)}"
            assert not results[0]["qc"]["errors"], f"{level}: {results[0]['qc']['errors']}"

    @check("cancellation: already-true should_cancel -> zero series")
    def _():
        in_dir, out_dir = _fresh_io()
        write_synthetic_series(in_dir, num_slices=3, modality="CT")
        cancelled = logic.process(
            in_dir, out_dir, load_into_scene=False, should_cancel=lambda: True
        )
        assert cancelled == [], f"expected no series when cancelled, got {len(cancelled)}"

    @check("empty folder raises a clear error")
    def _():
        in_dir, out_dir = _fresh_io()
        os.makedirs(in_dir, exist_ok=True)
        try:
            logic.process(in_dir, out_dir, load_into_scene=False)
        except RuntimeError:
            return
        raise AssertionError("expected RuntimeError for an empty input folder")

    @check("folder of non-DICOM junk raises, does not crash oddly")
    def _():
        in_dir, out_dir = _fresh_io()
        os.makedirs(in_dir, exist_ok=True)
        with open(os.path.join(in_dir, "notes.txt"), "w", encoding="utf-8") as fh:
            fh.write("this is not a DICOM file")
        try:
            logic.process(in_dir, out_dir, load_into_scene=False)
        except Exception:
            return
        raise AssertionError("expected an error for a folder with no readable DICOM")

    failures = []
    for name, fn in _CHECKS:
        slicer.mrmlScene.Clear()
        try:
            fn()
            log(f"  PASS  {name}")
        except Exception:
            failures.append(name)
            log(f"  FAIL  {name}")
            log(traceback.format_exc())
    return failures


status = 1
try:
    log(f"Slicer {slicer.app.applicationVersion} | Python {sys.version.split()[0]}")

    import DicomForgeBatch

    logic = DicomForgeBatch.DicomForgeBatchLogic()
    if not logic.is_dicom_forge_available():
        log("Installing dicom-anvil[convert] into Slicer's Python ...")
        logic.ensure_dependencies(with_convert=True)
    assert logic.is_dicom_forge_available(), "dicom-forge failed to install"

    import dicomforge

    log(f"dicom-anvil (import dicomforge): {dicomforge.__version__}")

    failures = _run_checks(logic)
    if failures:
        log(f"CI SELF-TEST FAILED ({len(failures)} of {len(_CHECKS)} checks failed)")
        status = 2
    else:
        log(f"CI SELF-TEST PASSED ({len(_CHECKS)} checks)")
        status = 0
except Exception:
    log("CI SELF-TEST FAILED (setup error)")
    log(traceback.format_exc())
    status = 2
finally:
    try:
        os.makedirs(os.path.dirname(RESULT_FILE), exist_ok=True)
        with open(RESULT_FILE, "w", encoding="utf-8") as fh:
            fh.write(f"EXIT_STATUS={status}\n")
            fh.write("\n".join(_log) + "\n")
    except Exception:
        traceback.print_exc()
    slicer.util.exit(status)
