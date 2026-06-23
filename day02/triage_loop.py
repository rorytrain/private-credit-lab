import os
import sys
import json
import csv
from datetime import datetime
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# GSAM Alternatives mandate parameters
MANDATE = {
    "min_ebitda_m": 10,
    "max_ebitda_m": 75,
    "max_leverage": 5.0,
    "excluded_sectors": ["retail", "energy", "oil", "gas"],
    "preferred_structures": ["unitranche", "term loan", "senior secured"],
    "sponsor_backed_required": True
}

LOG_FILE = "requests_log.txt"
CSV_FILE = "triage_results.csv"

CSV_HEADERS = [
    "file", "company_name", "sponsor", "sector",
    "revenue_m", "adjusted_ebitda_m", "unadjusted_ebitda_m", "addbacks_m",
    "facility_m", "leverage_x", "structure",
    "mandate_fit_score", "mandate_fit_rationale", "flags"
]

def load_cim(filepath):
    with open(filepath, "r") as f:
        return f.read()

def build_prompt(cim_text):
    return f"""You are a private credit analyst at a global alternatives platform.
You are triaging an incoming deal against the following mandate parameters:
- EBITDA range: ${MANDATE['min_ebitda_m']}m to ${MANDATE['max_ebitda_m']}m
- Maximum leverage: {MANDATE['max_leverage']}x
- Excluded sectors: {', '.join(MANDATE['excluded_sectors'])}
- Preferred structures: {', '.join(MANDATE['preferred_structures'])}
- Sponsor-backed deals only: {MANDATE['sponsor_backed_required']}

Review the following CIM and extract the key parameters. Note any add-backs
separately from adjusted EBITDA. Flag any elements that warrant credit scrutiny,
including dividend recapitalisations, aggressive add-backs or sector concerns.

Return your response as a JSON object with this exact structure:
{{
    "company_name": "",
    "sponsor": "",
    "sector": "",
    "revenue_m": 0,
    "adjusted_ebitda_m": 0,
    "unadjusted_ebitda_m": 0,
    "addbacks_m": 0,
    "facility_m": 0,
    "leverage_x": 0,
    "structure": "",
    "mandate_fit_score": 0,
    "mandate_fit_rationale": "",
    "flags": []
}}

Mandate fit score: 1 to 10, where 10 is a perfect fit.
Flags: a list of strings, each describing one concern in no more than two sentences.

CIM TEXT:
{cim_text}"""

def log_request(filepath, prompt, response_text):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write(f"TIMESTAMP : {datetime.now().isoformat()}\n")
        f.write(f"FILE      : {filepath}\n")
        f.write("-" * 40 + "\n")
        f.write("PROMPT:\n")
        f.write(prompt + "\n")
        f.write("-" * 40 + "\n")
        f.write("RESPONSE:\n")
        f.write(response_text + "\n")
        f.write("=" * 80 + "\n\n")

def triage_cim(filepath):
    cim_text = load_cim(filepath)
    prompt = build_prompt(cim_text)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = response.content[0].text
    log_request(filepath, prompt, response_text)

    clean = response_text.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(clean)

def write_csv_row(writer, filepath, result):
    writer.writerow({
        "file": filepath,
        "company_name": result.get("company_name", ""),
        "sponsor": result.get("sponsor", ""),
        "sector": result.get("sector", ""),
        "revenue_m": result.get("revenue_m", ""),
        "adjusted_ebitda_m": result.get("adjusted_ebitda_m", ""),
        "unadjusted_ebitda_m": result.get("unadjusted_ebitda_m", ""),
        "addbacks_m": result.get("addbacks_m", ""),
        "facility_m": result.get("facility_m", ""),
        "leverage_x": result.get("leverage_x", ""),
        "structure": result.get("structure", ""),
        "mandate_fit_score": result.get("mandate_fit_score", ""),
        "mandate_fit_rationale": result.get("mandate_fit_rationale", ""),
        "flags": " | ".join(result.get("flags", []))
    })

def main():
    if len(sys.argv) > 1:
        cim_files = sys.argv[1:]
    else:
        cim_files = [
            "sample_cim.txt",
            "sample_cim_2.txt",
            "sample_cim_3.txt"
        ]

    print(f"Processing {len(cim_files)} document(s)...\n")

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
        writer.writeheader()

        for filepath in cim_files:
            print(f"Triaging {filepath}...")
            try:
                result = triage_cim(filepath)
                write_csv_row(writer, filepath, result)
                print(f"  Score: {result.get('mandate_fit_score')} | {result.get('company_name')} | {result.get('sector')}")
            except Exception as e:
                print(f"  ERROR processing {filepath}: {e}")

    print(f"\nComplete. Results written to {CSV_FILE}")
    print(f"Request log written to {LOG_FILE}")

if __name__ == "__main__":
    main()