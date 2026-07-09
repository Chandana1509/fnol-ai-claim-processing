# import json
# import ollama


# def review_claim(fields):

#     prompt = f"""
# You are an insurance claim reviewer.

# Review the following extracted claim fields.

# {json.dumps(fields, indent=4)}

# Check for logical inconsistencies such as:

# - Incident Date before Policy Start Date
# - Incident Date after Policy Expiry
# - Estimated Damage unusually high
# - Missing important information
# - Contact number invalid
# - Asset ID suspicious
# - Policy Number format incorrect

# Return ONLY JSON.

# The JSON must be exactly like this:

# {{
#     "issues": [
#         "Issue 1",
#         "Issue 2"
#     ],
#     "confidence": "High"
# }}

# IMPORTANT:
# - issues must be a list of STRINGS.
# - Do NOT return dictionaries.
# - Do NOT explain anything.
# """

#     response = ollama.chat(
#         model="llama3.2",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     )

#     return json.loads(response["message"]["content"])






import json
import re
import ollama


def review_claim(fields):

    prompt = f"""
You are an Insurance Fraud Detection Assistant.

Analyze ONLY this claim description.

Description:

{fields.get("Description", "")}

Your job is ONLY to identify:

- Fraud indicators
- Staged accident indicators
- Suspicious wording
- Contradictory statements

DO NOT check:

- Policy Number
- Asset ID
- Contact Number
- Missing fields
- Dates
- Estimated Damage

Return ONLY JSON.

{{
    "issues": [
        "Possible staged accident.",
        "Description contains fraud-related keywords."
    ],
    "confidence": "Medium"
}}
"""

    response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    options={
        "num_predict": 300
    }
)

    content = response["message"]["content"].strip()

    print("\n========== OLLAMA RAW RESPONSE ==========")
    print(content)
    print("=========================================\n")

    return parse_ai_response(content)

def parse_ai_response(content):

    try:
        return json.loads(content)

    except json.JSONDecodeError:

    # If the response is missing the last closing brace,
    # append it and try again.

        if not content.strip().endswith("}"):

            try:
                return json.loads(content + "}")

            except:
                pass

    # Remove markdown if present

    content = content.replace("```json", "")
    content = content.replace("```", "")

    # Extract JSON object

    match = re.search(r"\{.*\}", content, re.DOTALL)

    if match:

        try:

            return json.loads(match.group())

        except:

            pass

    return {

        "issues":[

            "AI response could not be parsed."

        ],

        "confidence":"Unknown"

    }