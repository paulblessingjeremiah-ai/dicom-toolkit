"""Tests for the DICOM reader module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from pydicom.data import get_testdata_file
from dicom_toolkit.reader import read_dicom, get_metadata_summary


def test_read_dicom_returns_dataset():
    path = get_testdata_file("CT_small.dcm")
    ds = read_dicom(path)
    assert ds is not None
    assert ds.Modality == "CT"


def test_get_metadata_summary_has_expected_keys():
    path = get_testdata_file("CT_small.dcm")
    ds = read_dicom(path)
    summary = get_metadata_summary(ds)
    assert "Modality" in summary
    assert "Rows" in summary
    assert summary["Modality"] == "CT"


def test_get_metadata_summary_handles_missing_tags():
    path = get_testdata_file("MR_small.dcm")
    ds = read_dicom(path)
    summary = get_metadata_summary(ds)
    # Should not raise even if a tag like StudyDescription is missing
    assert "StudyDescription" in summary
