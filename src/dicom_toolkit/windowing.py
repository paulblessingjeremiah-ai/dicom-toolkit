"""CT windowing utilities for converting raw pixel data into viewable images."""

import numpy as np


# Common CT window presets (window center, window width) in Hounsfield Units
WINDOW_PRESETS = {
    "lung": (-600, 1500),
    "bone": (400, 1800),
    "soft_tissue": (40, 400),
    "brain": (40, 80),
}


def get_pixel_array_hu(ds):
    """Convert raw pixel data to Hounsfield Units using rescale slope/intercept."""
    pixel_array = ds.pixel_array.astype(np.float64)
    slope = getattr(ds, "RescaleSlope", 1)
    intercept = getattr(ds, "RescaleIntercept", 0)
    return pixel_array * slope + intercept


def apply_window(hu_array, window_center, window_width):
    """Apply a window level/width to an HU array, returning an 8-bit display image."""
    lower = window_center - window_width / 2
    upper = window_center + window_width / 2
    windowed = np.clip(hu_array, lower, upper)
    windowed = (windowed - lower) / (upper - lower) * 255.0
    return windowed.astype(np.uint8)


def apply_preset(hu_array, preset_name):
    """Apply a named window preset (lung, bone, soft_tissue, brain)."""
    if preset_name not in WINDOW_PRESETS:
        raise ValueError(f"Unknown preset: {preset_name}")
    center, width = WINDOW_PRESETS[preset_name]
    return apply_window(hu_array, center, width)
