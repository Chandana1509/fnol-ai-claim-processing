# validator.py

MANDATORY_FIELDS = [
    "Policy Number",
    "Policyholder Name",
    "Effective Dates",
    "Incident Date",
    "Incident Time",
    "Location",
    "Description",
    "Claimant",
    "Contact Details",
    "Asset Type",
    "Asset ID",
    "Estimated Damage",
    "Claim Type",
    "Attachments",
    "Initial Estimate"
]


def check_missing_fields(fields):

    missing = []

    invalid_values = [
        "",
        " ",
        "null",
        "none",
        "n/a",
        "na",
        "unknown"
    ]

    for field in MANDATORY_FIELDS:

        value = fields.get(field)

        if value is None:
            missing.append(field)
            continue

        value = str(value).strip().lower()

        if value in invalid_values:
            missing.append(field)

    return missing