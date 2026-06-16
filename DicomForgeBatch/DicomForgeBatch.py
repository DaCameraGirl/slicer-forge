"""DicomForgeBatch -- a 3D Slicer scripted module.

Batch-imports DICOM into Slicer by driving the headless ``dicom-forge`` pipeline:
each series is de-identified, quality-controlled, converted to NRRD, and loaded
into the scene. The heavy lifting lives in ``dicom-forge`` (a pip-installable,
independently tested library); this module is a thin Slicer GUI on top of it.

Slicer scripted modules follow a fixed four-class shape:

* ``DicomForgeBatch``        -- module metadata (title, category, help).
* ``DicomForgeBatchWidget``  -- the GUI panel and its event wiring.
* ``DicomForgeBatchLogic``   -- pure logic, usable headlessly and from tests.
* ``DicomForgeBatchTest``    -- self-test run by Slicer's testing framework.

Only ``slicer``/``qt``/``ctk``/``vtk`` (provided by the Slicer runtime) and
``dicom-forge`` are required; nothing here imports at module scope that would
prevent Slicer from loading the module when ``dicom-forge`` is not yet installed.
"""

from __future__ import annotations

import os
import traceback

import ctk
import qt
import slicer
from slicer.ScriptedLoadableModule import (
    ScriptedLoadableModule,
    ScriptedLoadableModuleLogic,
    ScriptedLoadableModuleTest,
    ScriptedLoadableModuleWidget,
)
from slicer.util import VTKObservationMixin

#: Minimum dicom-forge version this module is built against.
DICOM_FORGE_MIN_VERSION = "0.1.0"


# ---------------------------------------------------------------------------
# Module metadata
# ---------------------------------------------------------------------------
class DicomForgeBatch(ScriptedLoadableModule):
    """Module descriptor shown in Slicer's module list."""

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "DICOM Forge Batch"
        self.parent.categories = ["Informatics"]
        self.parent.dependencies = []
        self.parent.contributors = ["Angela Hudson (DaCameraGirl)"]
        self.parent.helpText = (
            "Batch-import DICOM into Slicer via the dicom-forge pipeline: "
            "de-identify, quality-control, convert to NRRD, and load each series "
            "into the scene. See the Dependencies section to install dicom-forge."
        )
        self.parent.acknowledgementText = (
            "Powered by dicom-forge (https://github.com/DaCameraGirl/dicom-forge)."
        )


# ---------------------------------------------------------------------------
# Logic (headless; no Qt)
# ---------------------------------------------------------------------------
class DicomForgeBatchLogic(ScriptedLoadableModuleLogic):
    """Headless logic that wraps the dicom-forge pipeline.

    Kept free of Qt so it can be exercised from the self-test and reused from
    other modules or the Python console.
    """

    @staticmethod
    def is_dicom_forge_available() -> bool:
        """Return True if the dicom-forge package can be imported."""
        try:
            import dicomforge  # noqa: F401
        except ImportError:
            return False
        return True

    @staticmethod
    def ensure_dependencies(*, with_convert: bool = True) -> None:
        """Install dicom-forge into Slicer's Python if it is missing.

        Uses ``slicer.util.pip_install`` so the package lands in the Slicer
        environment rather than the system Python. Safe to call repeatedly.
        """
        if DicomForgeBatchLogic.is_dicom_forge_available():
            return
        spec = "dicom-forge[convert]" if with_convert else "dicom-forge"
        slicer.util.pip_install(f"{spec}>={DICOM_FORGE_MIN_VERSION}")

    def process(
        self,
        input_dir: str,
        output_dir: str,
        *,
        deid_level: str = "moderate",
        output_format: str = "nrrd",
        load_into_scene: bool = True,
        progress_callback=None,
    ) -> list:
        """Run the pipeline over every series found under ``input_dir``.

        Parameters
        ----------
        input_dir, output_dir:
            Source DICOM tree and destination for converted volumes.
        deid_level:
            ``"basic"``, ``"moderate"``, or ``"strict"``.
        output_format:
            ``"nrrd"`` (recommended for Slicer) or ``"nifti"``.
        load_into_scene:
            When True, each converted volume is loaded into the Slicer scene.
        progress_callback:
            Optional ``callable(done, total, message)`` for UI progress.

        Returns
        -------
        list of dict
            One serialisable audit record per series processed.
        """
        if not self.is_dicom_forge_available():
            raise RuntimeError(
                "dicom-forge is not installed. Click 'Install / update dicom-forge' "
                "in the module panel, or run "
                "slicer.util.pip_install('dicom-forge[convert]')."
            )

        from dicomforge import PipelineConfig
        from dicomforge.config import DeidentificationLevel, OutputFormat
        from dicomforge.ingest import group_by_series, iter_dicom_files
        from dicomforge.pipeline import run_pipeline

        groups = group_by_series(iter_dicom_files(input_dir))
        if not groups:
            raise RuntimeError(f"No readable DICOM series found under: {input_dir}")

        config = PipelineConfig(
            deidentify=True,
            deidentification_level=DeidentificationLevel(deid_level),
            output_format=OutputFormat(output_format),
        )

        os.makedirs(output_dir, exist_ok=True)
        results = []
        series_uids = list(groups)
        total = len(series_uids)

        for index, series_uid in enumerate(series_uids):
            if progress_callback:
                progress_callback(index, total, f"Processing series {index + 1}/{total}")

            out_stem = os.path.join(output_dir, f"series_{index:03d}")
            result = run_pipeline(input_dir, out_stem, config=config, series_uid=series_uid)
            results.append(result.model_dump(mode="json"))

            if load_into_scene and result.conversion is not None:
                volume_node = slicer.util.loadVolume(result.conversion.output_path)
                volume_node.SetName(f"DICOMForge_{result.metadata.modality}_{index:03d}")

        if progress_callback:
            progress_callback(total, total, "Done")
        return results


# ---------------------------------------------------------------------------
# Widget (GUI)
# ---------------------------------------------------------------------------
class DicomForgeBatchWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """The module panel: input/output selectors, options, and a Run button."""

    def __init__(self, parent=None):
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)
        self.logic = DicomForgeBatchLogic()

    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)

        # --- Dependencies section ---
        dep_box = ctk.ctkCollapsibleButton()
        dep_box.text = "Dependencies"
        self.layout.addWidget(dep_box)
        dep_form = qt.QFormLayout(dep_box)

        self.statusLabel = qt.QLabel()
        dep_form.addRow("dicom-forge:", self.statusLabel)

        self.installButton = qt.QPushButton("Install / update dicom-forge")
        self.installButton.toolTip = (
            "Installs dicom-forge[convert] into Slicer's Python environment."
        )
        dep_form.addRow(self.installButton)

        # --- Input/output section ---
        io_box = ctk.ctkCollapsibleButton()
        io_box.text = "Input / Output"
        self.layout.addWidget(io_box)
        io_form = qt.QFormLayout(io_box)

        self.inputSelector = ctk.ctkPathLineEdit()
        self.inputSelector.filters = ctk.ctkPathLineEdit.Dirs
        self.inputSelector.toolTip = "Folder containing one or more DICOM series."
        io_form.addRow("DICOM folder:", self.inputSelector)

        self.outputSelector = ctk.ctkPathLineEdit()
        self.outputSelector.filters = ctk.ctkPathLineEdit.Dirs
        self.outputSelector.toolTip = "Destination for converted volumes."
        io_form.addRow("Output folder:", self.outputSelector)

        # --- Options section ---
        opt_box = ctk.ctkCollapsibleButton()
        opt_box.text = "Options"
        self.layout.addWidget(opt_box)
        opt_form = qt.QFormLayout(opt_box)

        self.deidCombo = qt.QComboBox()
        self.deidCombo.addItems(["basic", "moderate", "strict"])
        self.deidCombo.currentText = "moderate"
        self.deidCombo.toolTip = "How aggressively to remove patient-identifying data."
        opt_form.addRow("De-identification:", self.deidCombo)

        self.formatCombo = qt.QComboBox()
        self.formatCombo.addItems(["nrrd", "nifti"])
        self.formatCombo.toolTip = "NRRD is Slicer's native scalar volume format."
        opt_form.addRow("Output format:", self.formatCombo)

        self.loadCheck = qt.QCheckBox("Load converted volumes into the scene")
        self.loadCheck.checked = True
        opt_form.addRow(self.loadCheck)

        # --- Run ---
        self.runButton = qt.QPushButton("Run batch import")
        self.runButton.toolTip = "De-identify, QC, convert, and load every series."
        self.runButton.enabled = False
        self.layout.addWidget(self.runButton)

        self.progressBar = qt.QProgressBar()
        self.progressBar.visible = False
        self.layout.addWidget(self.progressBar)

        self.resultsView = qt.QTextEdit()
        self.resultsView.readOnly = True
        self.resultsView.setMinimumHeight(160)
        self.layout.addWidget(self.resultsView)

        self.layout.addStretch(1)

        # --- Connections ---
        self.installButton.connect("clicked(bool)", self.onInstall)
        self.runButton.connect("clicked(bool)", self.onRun)
        self.inputSelector.connect("currentPathChanged(QString)", self._update_run_state)
        self.outputSelector.connect("currentPathChanged(QString)", self._update_run_state)

        self._refresh_status()

    # -- helpers --
    def _refresh_status(self):
        available = self.logic.is_dicom_forge_available()
        self.statusLabel.text = "installed ✓" if available else "not installed"
        self.installButton.enabled = not available
        self._update_run_state()

    def _update_run_state(self, *_):
        self.runButton.enabled = (
            self.logic.is_dicom_forge_available()
            and bool(self.inputSelector.currentPath)
            and bool(self.outputSelector.currentPath)
        )

    def _on_progress(self, done, total, message):
        self.progressBar.maximum = max(total, 1)
        self.progressBar.value = done
        slicer.app.processEvents()

    # -- slots --
    def onInstall(self):
        with slicer.util.tryWithErrorDisplay("Failed to install dicom-forge."):
            slicer.util.showStatusMessage("Installing dicom-forge ...")
            self.logic.ensure_dependencies(with_convert=True)
            slicer.util.showStatusMessage("dicom-forge installed.", 2000)
        self._refresh_status()

    def onRun(self):
        self.progressBar.visible = True
        self.resultsView.clear()
        try:
            results = self.logic.process(
                self.inputSelector.currentPath,
                self.outputSelector.currentPath,
                deid_level=self.deidCombo.currentText,
                output_format=self.formatCombo.currentText,
                load_into_scene=self.loadCheck.checked,
                progress_callback=self._on_progress,
            )
            self._render_results(results)
        except Exception as exc:  # noqa: BLE001 - surface any failure to the user
            slicer.util.errorDisplay(f"Batch import failed:\n{exc}")
            self.resultsView.append(traceback.format_exc())
        finally:
            self.progressBar.visible = False

    def _render_results(self, results):
        lines = [f"Processed {len(results)} series:\n"]
        for r in results:
            qc = r["qc"]
            status = "PASS" if not qc["errors"] else "FAIL"
            lines.append(
                f"- {r['metadata']['modality']} "
                f"({qc['num_slices']} slices) QC={status} "
                f"-> {r['conversion']['output_path'] if r['conversion'] else 'n/a'}"
            )
            for w in qc["warnings"]:
                lines.append(f"    warning: {w}")
        self.resultsView.setPlainText("\n".join(lines))


# ---------------------------------------------------------------------------
# Self-test (run by Slicer's testing framework)
# ---------------------------------------------------------------------------
class DicomForgeBatchTest(ScriptedLoadableModuleTest):
    """Generates a synthetic series and exercises the logic end-to-end."""

    def setUp(self):
        slicer.mrmlScene.Clear()

    def runTest(self):
        self.setUp()
        self.test_batch_import()

    def test_batch_import(self):
        self.delayDisplay("Starting DicomForgeBatch self-test")
        logic = DicomForgeBatchLogic()
        logic.ensure_dependencies(with_convert=True)
        self.assertTrue(logic.is_dicom_forge_available())

        import tempfile

        from dicomforge_testdata import write_synthetic_series  # type: ignore

        with tempfile.TemporaryDirectory() as tmp:
            in_dir = os.path.join(tmp, "in")
            out_dir = os.path.join(tmp, "out")
            write_synthetic_series(in_dir, num_slices=6)

            results = logic.process(
                in_dir,
                out_dir,
                deid_level="moderate",
                output_format="nrrd",
                load_into_scene=True,
            )

            self.assertEqual(len(results), 1)
            self.assertTrue(results[0]["qc"]["geometry_consistent"])
            self.assertEqual(len(slicer.util.getNodesByClass("vtkMRMLScalarVolumeNode")), 1)
        self.delayDisplay("DicomForgeBatch self-test passed")
