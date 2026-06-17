"""Headless end-to-end self-test for CI.

Runs inside a real (headless) 3D Slicer:

    xvfb-run Slicer --no-splash --no-main-window --python-script ci_selftest.py

Adapted from ``scratch/run_live_test.py`` (which passed against Slicer 5.10).
It installs dicom-forge into Slicer's own Python via the module's own
``ensure_dependencies()`` -- so CI exercises the exact install path users hit --
generates a synthetic DICOM series, runs the pipeline end to end, asserts a
volume reached the MRML scene, and checks the cancellation path.

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


status = 1
try:
    log(f"Slicer {slicer.app.applicationVersion} | Python {sys.version.split()[0]}")

    import DicomForgeBatch

    logic = DicomForgeBatch.DicomForgeBatchLogic()
    if not logic.is_dicom_forge_available():
        log("Installing dicom-forge[convert] into Slicer's Python ...")
        logic.ensure_dependencies(with_convert=True)
    assert logic.is_dicom_forge_available(), "dicom-forge failed to install"

    import dicomforge

    log(f"dicom-forge: {dicomforge.__version__}")

    from dicomforge_testdata import write_synthetic_series

    slicer.mrmlScene.Clear()
    tmp = tempfile.mkdtemp()
    in_dir = os.path.join(tmp, "in")
    out_dir = os.path.join(tmp, "out")
    write_synthetic_series(in_dir, num_slices=6)
    log(f"Synthetic 6-slice CT series written to {in_dir}")

    results = logic.process(
        in_dir, out_dir, deid_level="moderate", output_format="nrrd", load_into_scene=True
    )
    vols = slicer.util.getNodesByClass("vtkMRMLScalarVolumeNode")
    assert len(results) == 1, f"expected 1 series, got {len(results)}"
    assert results[0]["qc"]["geometry_consistent"], results[0]["qc"]
    assert len(vols) == 1, f"expected 1 volume node in scene, got {len(vols)}"

    # Cancellation path: an already-true should_cancel must yield zero series.
    cancelled = logic.process(in_dir, out_dir, load_into_scene=False, should_cancel=lambda: True)
    assert cancelled == [], f"expected no series when cancelled, got {len(cancelled)}"

    log("CI SELF-TEST PASSED (pipeline end-to-end + cancellation)")
    status = 0
except Exception:
    log("CI SELF-TEST FAILED")
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
