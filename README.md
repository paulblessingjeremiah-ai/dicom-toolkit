# DICOM Toolkit

A Python toolkit for reading, inspecting, anonymising, and processing DICOM medical imaging data.

## Features

- DICOM metadata inspection
- Metadata anonymisation (removes or replaces identifying patient tags)
- Pixel-data extraction and Hounsfield Unit conversion
- CT windowing (lung, bone, soft tissue, brain presets)
- DICOM series loading and 3D volume reconstruction
- Automated tests

## Architecture


Each module is independent and can be used on its own or combined into a full pipeline.

## Example

```python
from dicom_toolkit.reader import read_dicom, get_metadata_summary
from dicom_toolkit.anonymizer import anonymize_dicom
from dicom_toolkit.windowing import get_pixel_array_hu, apply_preset

ds = read_dicom("scan.dcm")
print(get_metadata_summary(ds))

anonymized = anonymize_dicom(ds)

hu_array = get_pixel_array_hu(ds)
lung_view = apply_preset(hu_array, "lung")
```

Typical flow for a full series:

## Installation

```bash
pip install -r requirements.txt
```

## Running tests

```bash
pytest tests/
```

## Limitations

This toolkit is intended for educational and research purposes. It is not designed for clinical diagnosis or deployment in a clinical environment. The anonymizer removes a defined set of common identifying tags (PatientName, PatientID, PatientBirthDate, PatientAddress, PatientTelephoneNumbers, InstitutionName, ReferringPhysicianName) — it does not guarantee full de-identification or compliance with any specific regulation (e.g. HIPAA, GDPR).

## License

MIT
