# # consistency_checker.py

# import re
# from datetime import datetime


# def check_inconsistencies(fields):

#     inconsistent = []

#     # -------------------------------
#     # 1. Policy Number Format
#     # Expected: POL12345
#     # -------------------------------
#     policy = str(fields.get("Policy Number", "")).strip()

#     if policy:
#         if not re.match(r"^POL\d+$", policy):
#             inconsistent.append("Policy Number")

#     # -------------------------------
#     # 2. Contact Number
#     # Must contain exactly 10 digits
#     # -------------------------------
#     contact = str(fields.get("Contact Details", "")).strip()

#     if contact:
#         digits = re.sub(r"\D", "", contact)

#         if len(digits) != 10:
#             inconsistent.append("Contact Details")

#     # -------------------------------
#     # 3. Estimated Damage
#     # Must be numeric
#     # -------------------------------
#     damage = str(fields.get("Estimated Damage", "")).strip()

#     if damage:
#         numbers = re.sub(r"[^\d]", "", damage)

#         if numbers == "":
#             inconsistent.append("Estimated Damage")

#     # -------------------------------
#     # 4. Initial Estimate
#     # Must be numeric
#     # -------------------------------
#     estimate = str(fields.get("Initial Estimate", "")).strip()

#     if estimate:
#         numbers = re.sub(r"[^\d]", "", estimate)

#         if numbers == "":
#             inconsistent.append("Initial Estimate")

#     # -------------------------------
#     # 5. Compare Damage & Initial Estimate
#     # -------------------------------
#     try:

#         damage_value = int(
#             re.sub(r"[^\d]", "", damage)
#         )

#         estimate_value = int(
#             re.sub(r"[^\d]", "", estimate)
#         )

#         if damage_value != estimate_value:

#             inconsistent.append(
#                 "Estimated Damage / Initial Estimate"
#             )

#     except:
#         pass

#     # -------------------------------
#     # 6. Incident Date
#     # -------------------------------
#     incident = fields.get("Incident Date")

#     if incident:

#         valid = False

#         formats = [

#             "%d-%b-%Y",

#             "%d-%m-%Y",

#             "%d/%m/%Y",

#             "%Y-%m-%d",

#             "%d %B %Y"

#         ]

#         for fmt in formats:

#             try:

#                 incident_date = datetime.strptime(
#                     incident.strip(),
#                     fmt
#                 )

#                 valid = True

#                 break

#             except:

#                 pass

#         if not valid:

#             inconsistent.append("Incident Date")

#     # -------------------------------
#     # 7. Incident Date inside Policy Period
#     # -------------------------------
#     period = fields.get("Effective Dates")

#     if period and incident:

#         try:

#             start, end = period.split("to")

#             start = datetime.strptime(
#                 start.strip(),
#                 "%d-%b-%Y"
#             )

#             end = datetime.strptime(
#                 end.strip(),
#                 "%d-%b-%Y"
#             )

#             if incident_date < start:

#                 inconsistent.append(
#                     "Incident Date before Policy Start"
#                 )

#             if incident_date > end:

#                 inconsistent.append(
#                     "Incident Date after Policy Expiry"
#                 )

#         except:

#             pass

#     # -------------------------------
#     # 8. Asset ID
#     # Example:
#     # KA01AB1234
#     # -------------------------------
#     asset = str(fields.get("Asset ID", "")).strip()

#     if asset:

#         if len(asset) < 8:

#             inconsistent.append("Asset ID")

#     return list(set(inconsistent))


import re
from datetime import datetime


def check_inconsistencies(fields):

    issues = []

    # Policy Number format
    policy = str(fields.get("Policy Number", ""))

    if policy and not re.match(r"^POL\d{5}$", policy):
        issues.append("Policy Number format is invalid.")

    # Contact Number
    contact = str(fields.get("Contact Details", ""))

    if contact and not re.match(r"^[6-9]\d{9}$", contact):
        issues.append("Contact number format is invalid.")

    # Asset ID
    asset = str(fields.get("Asset ID", ""))

    if asset and not re.match(r"^[A-Z]{2}\d{3}$", asset):
        issues.append("Asset ID format is invalid.")

    # Effective Dates
    effective = fields.get("Effective Dates")

    incident = fields.get("Incident Date")

    if effective and incident:

        try:

            start, end = effective.split("to")

            start = datetime.strptime(start.strip(), "%d-%b-%Y")

            end = datetime.strptime(end.strip(), "%d-%b-%Y")

            incident = datetime.strptime(incident.strip(), "%d-%b-%Y")

            if incident < start:

                issues.append(
                    "Incident occurred before policy start date."
                )

            if incident > end:

                issues.append(
                    "Incident occurred after policy expiry."
                )

        except:

            pass

    return issues
