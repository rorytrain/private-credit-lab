import sys
import os
import json
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

def load_cim(filepath):
    with open(filepath, "r") as f:
        return f.read()

def triage_cim(cim_text):
    prompt = f"""You are a private credit analyst at a global alternatives platform.
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

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.content[0].text
    clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(clean)

def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else "sample_cim.txt"
    cim_text = load_cim(filepath)
    print(f"Running triage on {filepath}...\n")
    result = triage_cim(cim_text)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()