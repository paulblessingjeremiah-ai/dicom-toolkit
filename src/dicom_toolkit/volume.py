"""Utilities for loading a DICOM series and reconstructing a 3D volume."""

import os
import numpy as np
import pydicom


def load_series(folder_path):
    """Load all DICOM files in a folder and return them sorted by slice position."""
    datasets = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        try:
            ds = pydicom.dcmread(filepath)
            datasets.append(ds)
        except Exception:
            # Skip files that aren't valid DICOM
            continue

    if not datasets:
        raise ValueError(f"No valid DICOM files found in {folder_path}")

    datasets = sort_slices(datasets)
    return datasets


def sort_slices(datasets):
    """Sort DICOM datasets by their position along the slice axis."""
    def get_position(ds):
        if hasattr(ds, "ImagePositionPatient"):
            return float(ds.ImagePositionPatient[2])
        elif hasattr(ds, "InstanceNumber"):
            return int(ds.InstanceNumber)
        return 0

    return sorted(datasets, key=get_position)


def build_volume(datasets):
    """Stack sorted DICOM datasets into a single 3D numpy array."""
    slices = [ds.pixel_array for ds in datasets]
    return np.stack(slices, axis=0)
