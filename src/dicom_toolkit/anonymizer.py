"""DICOM anonymization utilities."""


ANONYMIZE_TAGS = {
    "PatientName": "ANONYMOUS",
    "PatientID": "ANONYMOUS",
    "PatientBirthDate": "",
    "PatientAddress": "",
    "PatientTelephoneNumbers": "",
    "InstitutionName": "",
    "ReferringPhysicianName": "",
}


def anonymize_dicom(ds):
    """Return a copy of the dataset with identifying tags removed or replaced."""
    anonymized = ds.copy()
    for tag, replacement in ANONYMIZE_TAGS.items():
        if hasattr(anonymized, tag):
            setattr(anonymized, tag, replacement)
    return anonymized
