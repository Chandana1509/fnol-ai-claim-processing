from flask import Flask, render_template, request
import json
import os

from extractor import extract_fields
from validator import check_missing_fields
from router import decide_route
from pdf_reader import read_pdf
from consistency_checker import check_inconsistencies
from flask import send_file
import time
from reviewer import review_claim

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    if request.method == "POST":

        if "file" not in request.files:

            return render_template(
                "index.html",
                error="No file selected."
            )

        uploaded_file = request.files["file"]

        if uploaded_file.filename == "":

            return render_template(
                "index.html",
                error="Please choose a file."
            )

        filename = uploaded_file.filename.lower()

        if not (
            filename.endswith(".pdf")
            or filename.endswith(".txt")
        ):

            return render_template(
                "index.html",
                error="Only PDF and TXT files are supported."
            )

        start_time = time.time()

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            uploaded_file.filename
        )

        uploaded_file.save(file_path)

        try:

            if filename.endswith(".pdf"):

                text = read_pdf(file_path)

            else:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    text = file.read()

            if text.strip() == "":

                return render_template(
                    "index.html",
                    error="Uploaded file contains no readable text."
                )

           
            fields = extract_fields(text)

# Missing fields
            missing_fields = check_missing_fields(fields)

# Rule-based inconsistencies
            rule_issues = check_inconsistencies(fields)

# AI review
            ai_review = review_claim(fields)

            ai_issues = ai_review.get("issues", [])
            print("\n===== AI ISSUES =====")

            for issue in ai_issues:
                print(issue)
                print(type(issue))

                print("====================\n")

            filtered_ai_issues = []

            for issue in ai_issues:

    # If AI returned an object
                if isinstance(issue, dict):

                    if "description" in issue:
                        issue = issue["description"]

                    elif "message" in issue:
                        issue = issue["message"]

                    elif "reason" in issue:
                        issue = issue["reason"]

                    else:
                        issue = str(issue)

                issue = str(issue)

                issue_lower = issue.lower()

    # Ignore unwanted AI messages

                if "policyholder" in issue_lower:
                    continue

                if "contact" in issue_lower:
                    continue

                if "asset id format" in issue_lower:
                    continue

                if "asset type" in issue_lower:
                    continue

                if "missing field" in issue_lower:
                    continue

                filtered_ai_issues.append(issue)

# Merge both
            inconsistent_fields = rule_issues.copy()

            for issue in filtered_ai_issues:

                if issue not in inconsistent_fields:

                    inconsistent_fields.append(issue)

    #         try:
    #             ai_review = review_claim(fields)
    #             print("\n===== AI REVIEW =====")
    #             print(ai_review)
    #             print(type(ai_review))
    #             print("====================")
    #         except Exception as e:
    #             print("AI Review Error:", e)

    #             ai_review = {
    #     "issues": [],
    #     "confidence": "Unknown"
    # }

            missing_fields = check_missing_fields(fields)

            inconsistent_fields = check_inconsistencies(fields)

            for issue in ai_review.get("issues", []):

                if isinstance(issue, dict):

                    issue = (
            issue.get("reason")
            or issue.get("message")
            or issue.get("issue")
            or json.dumps(issue)
        )

                issue = str(issue)

                if issue not in inconsistent_fields:

                    inconsistent_fields.append(issue)

            route, reason = decide_route(
                fields,
                missing_fields,
                inconsistent_fields
            )

            # Determine Claim Status

            if route == "Fast-track":

                claim_status = "🟢 Eligible for Fast-track Processing"

            elif route == "Manual Review":

                claim_status = "🟡 Pending Manual Review"

            elif route == "Investigation Flag":

                claim_status = "🟠 Under Investigation"

            elif route == "Specialist Queue":

                claim_status = "🔵 Awaiting Specialist Review"

            else:

                claim_status = "⚪ Pending Standard Review"

            end_time = time.time()

            processing_time = round(
                end_time - start_time,
                2
            )

            # Calculate confidence based on validation results

            if len(missing_fields) == 0 and len(inconsistent_fields) == 0:
                confidence = "High"

            elif len(missing_fields) <= 2 and len(inconsistent_fields) <= 2:
                confidence = "Medium"

            else:
                confidence = "Low"


            result = {

    "fileName": uploaded_file.filename,

    "processingTime":
        f"{processing_time} seconds",

    "confidence": confidence,

    "extractedFields": fields,

    "missingFields": missing_fields,

    "inconsistentFields":
        inconsistent_fields,

    "recommendedRoute": route,

    "claimStatus": claim_status,

    "reasoning": reason

}

            with open(
                "output/result.json",
                "w",
                encoding="utf-8"
            ) as outfile:

                json.dump(
                    result,
                    outfile,
                    indent=4,
                    ensure_ascii=False
                )

        except Exception as e:

            return render_template(
                "index.html",
                error=f"Error: {str(e)}"
            )

    return render_template(
        "index.html",
        result=result
    )




@app.route("/download")
def download():

    return send_file(
        "output/result.json",
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)