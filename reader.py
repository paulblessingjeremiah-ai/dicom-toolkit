"""DICOM reading and metadata extraction utilities."""

import pydicom


def read_dicom(path):
    """Read a DICOM file and return the dataset."""
    return pydicom.dcmread(path)


def get_metadata_summary(ds):
    """Extract key metadata into a clean dictionary."""
    return {
        "Modality": getattr(ds, "Modality", None),
        "Rows": getattr(ds, "Rows", None),
        "Columns": getattr(ds, "Columns", None),
        "PixelSpacing": getattr(ds, "PixelSpacing", None),
        "SliceThickness": getattr(ds, "SliceThickness", None),
        "StudyDate": getattr(ds, "StudyDate", None),
        "StudyDescription": getattr(ds, "StudyDescription", None),
    }
