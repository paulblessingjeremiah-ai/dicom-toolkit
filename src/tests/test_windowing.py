"""Tests for CT windowing utilities."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np
from dicom_toolkit.windowing import apply_window, apply_preset, WINDOW_PRESETS


def test_apply_window_output_range():
    hu_array = np.array([[-1000, 0, 1000], [500, -500, 200]])
    result = apply_window(hu_array, window_center=40, window_width=400)
    assert result.min() >= 0
    assert result.max() <= 255
    assert result.dtype == np.uint8


def test_apply_preset_known_name():
    hu_array = np.array([[0, 100], [200, 300]])
    result = apply_preset(hu_array, "soft_tissue")
    assert result.shape == hu_array.shape


def test_apply_preset_unknown_name_raises():
    hu_array = np.array([[0, 100]])
    try:
        apply_preset(hu_array, "not_a_real_preset")
        assert False, "Expected ValueError"
    except ValueError:
        pass
