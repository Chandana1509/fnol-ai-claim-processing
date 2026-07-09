import re

def decide_route(fields, missing_fields, inconsistent_fields):

    description = str(fields.get("Description", "")).lower()

    fraud_keywords = [
        "fraud",
        "staged",
        "inconsistent",
        "fake",
        "suspicious",
        "intentional"
    ]

    if any(word in description for word in fraud_keywords):
        return (
            "Investigation Flag",
            "Fraud or suspicious keywords detected in the claim description."
        )

    claim_type = str(fields.get("Claim Type", "")).lower()

    if "injury" in claim_type:
        return (
            "Specialist Queue",
            "Claim involves bodily injury."
        )

    if missing_fields:
        return (
            "Manual Review",
            f"Mandatory fields missing: {', '.join(missing_fields)}."
        )

    damage = str(fields.get("Estimated Damage", "0"))
    damage = re.sub(r"[^\d]", "", damage)
    damage = int(damage) if damage else 0

    if damage < 25000:
        return (
            "Fast-track",
            f"Estimated damage (Rs. {damage}) is below Rs. 25,000."
        )

    return (
        "Standard Processing",
        "Claim requires standard assessment."
    )