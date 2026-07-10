import os
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Internal credit standard — deviations from these thresholds are flagged
INTERNAL_STANDARD = {
    "max_leverage_initial": 4.50,
    "max_leverage_steady_state": 4.00,
    "min_liquidity_m": 2.5,
    "max_capex_m": 5.0,
    "restricted_payments_leverage_threshold": 3.50,
    "restricted_payments_min_liquidity_m": 4.0,
    "max_reporting_delay_monthly_days": 30,
    "max_reporting_delay_quarterly_days": 45,
    "max_reporting_delay_annual_days": 120,
    "max_cure_period_days": 30,
    "equity_cure_permitted": False
}

def load_agreement(filepath):
    with open(filepath, "r") as f:
        return f.read()

def compare_covenants(agreement_a_text, agreement_b_text):
    prompt = f"""You are a senior credit analyst at a global alternatives platform.
You have been given two credit agreements and an internal covenant standard.
Your task is to:
1. Extract the key covenant terms from each agreement
2. Compare the two agreements against each other
3. Flag any deviation from the internal standard in either agreement

Internal covenant standard:
- Maximum initial leverage: {INTERNAL_STANDARD['max_leverage_initial']}x
- Maximum steady state leverage: {INTERNAL_STANDARD['max_leverage_steady_state']}x
- Minimum liquidity: ${INTERNAL_STANDARD['min_liquidity_m']}m
- Maximum annual capex: ${INTERNAL_STANDARD['max_capex_m']}m
- Restricted payments leverage threshold: {INTERNAL_STANDARD['restricted_payments_leverage_threshold']}x
- Restricted payments minimum liquidity: ${INTERNAL_STANDARD['restricted_payments_min_liquidity_m']}m
- Maximum monthly reporting delay: {INTERNAL_STANDARD['max_reporting_delay_monthly_days']} days
- Maximum quarterly reporting delay: {INTERNAL_STANDARD['max_reporting_delay_quarterly_days']} days
- Maximum annual reporting delay: {INTERNAL_STANDARD['max_reporting_delay_annual_days']} days
- Maximum cure period: {INTERNAL_STANDARD['max_cure_period_days']} days
- Equity cure permitted: {INTERNAL_STANDARD['equity_cure_permitted']}

Return your response as a JSON object with this exact structure:
{{
    "agreement_a": {{
        "borrower": "",
        "facility_m": 0,
        "covenants": {{
            "leverage_initial_x": 0,
            "leverage_steady_state_x": 0,
            "min_liquidity_m": 0,
            "max_capex_m": 0,
            "restricted_payments_leverage_threshold_x": 0,
            "restricted_payments_min_liquidity_m": 0,
            "monthly_reporting_days": 0,
            "quarterly_reporting_days": 0,
            "annual_reporting_days": 0,
            "cure_period_days": 0,
            "equity_cure_permitted": false
        }}
    }},
    "agreement_b": {{
        "borrower": "",
        "facility_m": 0,
        "covenants": {{
            "leverage_initial_x": 0,
            "leverage_steady_state_x": 0,
            "min_liquidity_m": 0,
            "max_capex_m": 0,
            "restricted_payments_leverage_threshold_x": 0,
            "restricted_payments_min_liquidity_m": 0,
            "monthly_reporting_days": 0,
            "quarterly_reporting_days": 0,
            "annual_reporting_days": 0,
            "cure_period_days": 0,
            "equity_cure_permitted": false
        }}
    }},
    "deviations": [
        {{
            "covenant": "",
            "agreement": "",
            "internal_standard": "",
            "actual": "",
            "severity": "",
            "note": ""
        }}
    ],
    "summary": ""
}}

Severity must be one of: HIGH, MEDIUM, LOW.
Each deviation note must be no more than two sentences.
The summary must be no more than three sentences covering overall credit quality
difference between the two agreements.

AGREEMENT A:
{agreement_a_text}

AGREEMENT B:
{agreement_b_text}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.content[0].text
    clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(clean)

def main():
    print("Loading credit agreements...\n")
    agreement_a = load_agreement("credit_agreement_apex.txt")
    agreement_b = load_agreement("credit_agreement_harrier.txt")

    print("Running covenant comparison...\n")
    result = compare_covenants(agreement_a, agreement_b)

    print(json.dumps(result, indent=2))

    with open("covenant_comparison.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("\nOutput written to covenant_comparison.json")

if __name__ == "__main__":
    main()