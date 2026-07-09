# 🛡️ FNOL Claim Processing Agent

## video walkthrough
https://drive.google.com/file/d/1EFIKPtoNMaLRzao0Vhr1vm8wqTdClSXv/view?usp=sharing

or

https://www.loom.com/share/3f427220ba3e4ffeaac8c217af4e99c5

## Overview

The **FNOL (First Notice of Loss) Claim Processing Agent** is an AI-powered application that automates the initial processing of insurance claim documents.

The system accepts FNOL documents in **PDF** and **TXT** formats, extracts key claim information using **Ollama (Llama 3.2)**, validates the extracted data, applies predefined business rules, and recommends the appropriate claim processing workflow.

This project was developed as part of an AI assessment to demonstrate document understanding, information extraction, rule-based reasoning, and workflow automation.

---

# Features

- Upload FNOL documents (PDF/TXT)
- AI-powered information extraction using Ollama (Llama 3.2)
- Automatic extraction of policy, incident, claimant, and asset information
- Validation of mandatory fields
- Detection of inconsistent data
- Rule-based claim routing
- Human-readable explanation for routing decisions
- JSON output generation
- Simple and responsive web interface using Flask

---

# Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Backend Development |
| Flask | Web Framework |
| Ollama | Local LLM Runtime |
| Llama 3.2 | AI Model for Information Extraction |
| PDFPlumber | PDF Text Extraction |
| HTML5 | Frontend |
| CSS3 | Styling |

---

# System Architecture

```
                    User Upload
                         │
                         ▼
               PDF / TXT Document
                         │
                         ▼
                 PDF Text Extraction
                         │
                         ▼
               Ollama (Llama 3.2 AI)
                         │
                         ▼
               Structured JSON Output
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
 Missing Field Validation      Consistency Check
          │                             │
          └──────────────┬──────────────┘
                         ▼
                 Routing Decision Engine
                         │
                         ▼
                  Final JSON Response
                         │
                         ▼
                    Flask Web UI
```

---

# Project Structure

```
FNOL-Agent/
│
├── app.py
├── extractor.py
├── llm.py
├── prompts.py
├── pdf_reader.py
├── validator.py
├── consistency_checker.py
├── router.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── uploads/
├── output/
└── sample_docs/
```

---

# Business Rules

The routing engine follows these rules:

| Condition | Route |
|-----------|-------|
| Estimated Damage < ₹25,000 | Fast-track |
| Missing Mandatory Fields | Manual Review |
| Inconsistent Data | Manual Review |
| Description contains fraud / staged / inconsistent | Investigation Flag |
| Claim Type = Injury | Specialist Queue |
| Otherwise | Standard Processing |

---

# Extracted Fields

### Policy Information

- Policy Number
- Policyholder Name
- Effective Dates

### Incident Information

- Incident Date
- Incident Time
- Location
- Description

### Involved Parties

- Claimant
- Third Parties
- Contact Details

### Asset Details

- Asset Type
- Asset ID
- Estimated Damage

### Other Information

- Claim Type
- Attachments
- Initial Estimate

---

# Application Workflow

1. User uploads an FNOL document.
2. The system extracts text from the uploaded document.
3. Ollama (Llama 3.2) analyzes the document.
4. AI extracts structured claim information.
5. Mandatory fields are validated.
6. Inconsistent values are detected.
7. Business routing rules are applied.
8. The final JSON response is generated.
9. Results are displayed on the web interface.

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/yourusername/FNOL-Agent.git
```

```bash
cd FNOL-Agent
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Install Ollama

Download Ollama:

https://ollama.com/download

Pull the required model:

```bash
ollama pull llama3.2
```

Start Ollama

```bash
ollama serve
```

---

# Run the Application

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

Upload an FNOL PDF or TXT document and click **Analyze Claim**.

---

# Sample JSON Output

```json
{
    "extractedFields": {},
    "missingFields": [],
    "inconsistentFields": [],
    "recommendedRoute": "Fast-track",
    "reasoning": "Estimated damage is below ₹25,000."
}
```

---

# Future Improvements

- OCR support for scanned documents
- Database integration
- User authentication
- Claim history dashboard
- Confidence score for extracted fields
- Multi-language document support

---



# Author

**Chandana C M**

Computer Science & Engineering (Data Science)

AI | Python | Flask | Machine Learning
