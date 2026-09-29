"""Tests for the DICOM anonymizer."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from pydicom.data import get_testdata_file
from dicom_toolkit.reader import read_dicom
from dicom_toolkit.anonymizer import anonymize_dicom


def test_anonymize_removes_patient_name():
    path = get_testdata_file("CT_small.dcm")
    ds = read_dicom(path)
    anonymized = anonymize_dicom(ds)
    assert anonymized.PatientName == "ANONYMOUS"


def test_anonymize_does_not_mutate_original():
    path = get_testdata_file("CT_small.dcm")
    ds = read_dicom(path)
    original_name = ds.PatientName
    anonymize_dicom(ds)
    assert ds.PatientName == original_name
