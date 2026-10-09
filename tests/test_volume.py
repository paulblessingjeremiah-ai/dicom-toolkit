"""Tests for series loading and volume reconstruction.

These build a fake series from pydicom's bundled CT sample, so no real patient data is needed.
Each fake slice gets a different z position, and the order is shuffled on purpose.
"""

import copy
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pydicom
import pytest
from pydicom.data import get_testdata_file
from dicom_toolkit.volume import build_volume, load_series, sort_slices


def make_series(n=6):
    base = pydicom.dcmread(get_testdata_file("CT_small.dcm"))
    slices = []
    for i in range(n):
        ds = copy.deepcopy(base)
        ds.ImagePositionPatient = [0.0, 0.0, float(i) * 2.5]
        ds.InstanceNumber = n - i  # instance numbers run the opposite way, so sorting must use position
        slices.append(ds)
    random.Random(0).shuffle(slices)
    return slices, base


def test_sort_slices_orders_by_physical_position_not_instance_number():
    slices, _ = make_series()
    ordered = sort_slices(slices)
    z = [float(ds.ImagePositionPatient[2]) for ds in ordered]
    assert z == sorted(z)


def test_sort_slices_falls_back_to_instance_number():
    slices, _ = make_series()
    for ds in slices:
        del ds.ImagePositionPatient
    ordered = sort_slices(slices)
    numbers = [int(ds.InstanceNumber) for ds in ordered]
    assert numbers == sorted(numbers)


def test_build_volume_stacks_slices_along_first_axis():
    slices, base = make_series(n=6)
    volume = build_volume(sort_slices(slices))
    assert volume.shape == (6, base.Rows, base.Columns)


def test_load_series_skips_non_dicom_files_and_sorts(tmp_path):
    slices, _ = make_series(n=5)
    for i, ds in enumerate(slices):
        ds.save_as(str(tmp_path / f"file_{i}.dcm"))
    (tmp_path / "notes.txt").write_text("not a dicom file")

    loaded = load_series(str(tmp_path))
    z = [float(ds.ImagePositionPatient[2]) for ds in loaded]
    assert len(loaded) == 5
    assert z == sorted(z)


def test_load_series_raises_on_empty_folder(tmp_path):
    with pytest.raises(ValueError):
        load_series(str(tmp_path))
