"""Synthetic DICOM generation for the DicomForgeBatch self-test.

Lets the Slicer self-test run without any real patient data: it writes small,
valid series (with deliberate PHI tags) to a directory so the full pipeline can
be exercised. Mirrors the generator used in dicom-forge's own test suite.
"""

from __future__ import annotations

import os

import numpy as np
import pydicom
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import (
    CTImageStorage,
    ExplicitVRLittleEndian,
    MRImageStorage,
    generate_uid,
)

#: SOP Class UID per supported synthetic modality.
_SOP_CLASS_FOR_MODALITY = {
    "CT": CTImageStorage,
    "MR": MRImageStorage,
}


def write_synthetic_series(
    directory: str,
    *,
    num_slices: int = 6,
    rows: int = 16,
    cols: int = 16,
    modality: str = "CT",
    prefix: str = "slice",
    series_uid: str | None = None,
    study_uid: str | None = None,
) -> str:
    """Write a single synthetic series to ``directory`` and return that path.

    ``modality`` is ``"CT"`` or ``"MR"`` (sets the SOP Class UID and the
    Modality tag). ``prefix`` names the files, so several series can share a
    directory without colliding. ``series_uid``/``study_uid`` let a caller place
    multiple series under one study; both default to fresh UIDs.
    """
    if modality not in _SOP_CLASS_FOR_MODALITY:
        raise ValueError(f"unsupported synthetic modality: {modality!r}")
    sop_class = _SOP_CLASS_FOR_MODALITY[modality]

    os.makedirs(directory, exist_ok=True)
    study_uid = study_uid or generate_uid()
    series_uid = series_uid or generate_uid()

    for index in range(num_slices):
        file_meta = FileMetaDataset()
        file_meta.MediaStorageSOPClassUID = sop_class
        file_meta.MediaStorageSOPInstanceUID = generate_uid()
        file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

        ds = Dataset()
        ds.file_meta = file_meta
        ds.SOPClassUID = sop_class
        ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
        ds.StudyInstanceUID = study_uid
        ds.SeriesInstanceUID = series_uid
        ds.Modality = modality
        ds.Manufacturer = "ForgeSim"
        ds.InstanceNumber = index + 1

        ds.Rows = rows
        ds.Columns = cols
        ds.PixelSpacing = [0.7, 0.7]
        ds.SliceThickness = 1.0
        ds.ImageOrientationPatient = [1, 0, 0, 0, 1, 0]
        ds.ImagePositionPatient = [0.0, 0.0, float(index)]
        # Rescale tags are a CT convention (Hounsfield units); MR doesn't use them.
        if modality == "CT":
            ds.RescaleSlope = 1
            ds.RescaleIntercept = -1024

        base = np.linspace(0, 2000, rows * cols, dtype=np.int16).reshape(rows, cols)
        arr = (base + index * 10).astype(np.int16)
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.BitsAllocated = 16
        ds.BitsStored = 16
        ds.HighBit = 15
        ds.PixelRepresentation = 1
        ds.PixelData = arr.tobytes()

        # Deliberate PHI so the de-identification path is exercised.
        ds.PatientName = "DOE^JANE"
        ds.PatientID = "MRN-0001"
        ds.PatientBirthDate = "19700101"
        ds.InstitutionName = "General Hospital"

        _save_dataset(ds, os.path.join(directory, f"{prefix}_{index:03d}.dcm"))

    return directory


def write_multiple_series(
    directory: str,
    *,
    modalities: list[str] | None = None,
    num_slices: int = 4,
) -> str:
    """Write several series into one ``directory`` under a shared study.

    Each series gets a distinct SeriesInstanceUID and file prefix, so
    ``group_by_series`` must split them apart. Defaults to one CT and one MR.
    """
    modalities = modalities or ["CT", "MR"]
    study_uid = generate_uid()
    for series_index, modality in enumerate(modalities):
        write_synthetic_series(
            directory,
            num_slices=num_slices,
            modality=modality,
            prefix=f"s{series_index}",
            series_uid=generate_uid(),
            study_uid=study_uid,
        )
    return directory


def _save_dataset(ds: Dataset, path: str) -> None:
    """Write a proper file-format DICOM across pydicom versions.

    pydicom 3.0 renamed the flag that writes the 128-byte preamble + 'DICM'
    marker from ``write_like_original=False`` to ``enforce_file_format=True``.
    3D Slicer may bundle either generation, so we try the new API first and
    fall back to the legacy one.
    """
    try:
        ds.save_as(path, enforce_file_format=True)
    except TypeError:
        ds.save_as(path, write_like_original=False)


# Allow ``python dicomforge_testdata.py <dir>`` for quick manual fixture creation.
if __name__ == "__main__":  # pragma: no cover
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "synthetic_series"
    print("wrote", write_synthetic_series(target))
    print("pydicom", pydicom.__version__)
