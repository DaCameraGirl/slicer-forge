"""Synthetic DICOM generation for the DicomForgeBatch self-test.

Lets the Slicer self-test run without any real patient data: it writes a small,
valid CT series (with deliberate PHI tags) to a directory so the full pipeline
can be exercised. Mirrors the generator used in dicom-forge's own test suite.
"""

from __future__ import annotations

import os

import numpy as np
import pydicom
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import CTImageStorage, ExplicitVRLittleEndian, generate_uid


def write_synthetic_series(
    directory: str, *, num_slices: int = 6, rows: int = 16, cols: int = 16
) -> str:
    """Write a synthetic CT series to ``directory`` and return that path."""
    os.makedirs(directory, exist_ok=True)
    study_uid = generate_uid()
    series_uid = generate_uid()

    for index in range(num_slices):
        file_meta = FileMetaDataset()
        file_meta.MediaStorageSOPClassUID = CTImageStorage
        file_meta.MediaStorageSOPInstanceUID = generate_uid()
        file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

        ds = Dataset()
        ds.file_meta = file_meta
        ds.SOPClassUID = CTImageStorage
        ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
        ds.StudyInstanceUID = study_uid
        ds.SeriesInstanceUID = series_uid
        ds.Modality = "CT"
        ds.Manufacturer = "ForgeSim"
        ds.InstanceNumber = index + 1

        ds.Rows = rows
        ds.Columns = cols
        ds.PixelSpacing = [0.7, 0.7]
        ds.SliceThickness = 1.0
        ds.ImageOrientationPatient = [1, 0, 0, 0, 1, 0]
        ds.ImagePositionPatient = [0.0, 0.0, float(index)]
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

        _save_dataset(ds, os.path.join(directory, f"slice_{index:03d}.dcm"))

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
