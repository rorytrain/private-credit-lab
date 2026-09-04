import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

COVENANTS = {
    "max_leverage_x": 4.25,
    "min_liquidity_m": 3.0,
    "max_capex_ytd_m": 4.0,
    "min_interest_coverage_x": 3.0
}

def load_update(filepath):
    with open(filepath, "r") as f:
        return f.read()

def extract_metrics(update_text):
    prompt = f"""You are a credit monitoring analyst at a private credit platform.
Extract the following financial metrics from the borrower update below.
Return only a JSON object with this exact structure and no other text:
{{
    "borrower": "",
    "reporting_period": "",
    "revenue_ltm_m": 0,
    "adjusted_ebitda_ltm_m": 0,
    "unadjusted_ebitda_ltm_m": 0,
    "addbacks_m": 0,
    "cash_m": 0,
    "total_debt_m": 0,
    "net_debt_m": 0,
    "leverage_x": 0,
    "interest_coverage_x": 0,
    "capex_ytd_m": 0,
    "borrower_compliance_statement": ""
}}

If a field is not present in the document use null.
The borrower_compliance_statement should be a one-sentence summary
of what the borrower says about covenant compliance.

BORROWER UPDATE:
{update_text}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text
    clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(clean)

def run_covenant_checks(metrics):
    breaches = []
    warnings = []

    leverage = metrics.get("leverage_x")
    if leverage is not None:
        if leverage > COVENANTS["max_leverage_x"]:
            breaches.append({
                "covenant": "Maximum Leverage",
                "threshold": str(COVENANTS["max_leverage_x"]) + "x",
                "actual": str(leverage) + "x",
                "breach": True,
                "note": "Leverage of " + str(leverage) + "x exceeds the " + str(COVENANTS["max_leverage_x"]) + "x covenant threshold."
            })
        elif leverage > COVENANTS["max_leverage_x"] * 0.90:
            warnings.append({
                "covenant": "Maximum Leverage",
                "threshold": str(COVENANTS["max_leverage_x"]) + "x",
                "actual": str(leverage) + "x",
                "breach": False,
                "note": "Leverage of " + str(leverage) + "x is within 10pct of the " + str(COVENANTS["max_leverage_x"]) + "x covenant threshold. Monitor closely."
            })

    liquidity = metrics.get("cash_m")
    if liquidity is not None:
        if liquidity < COVENANTS["min_liquidity_m"]:
            breaches.append({
                "covenant": "Minimum Liquidity",
                "threshold": "$" + str(COVENANTS["min_liquidity_m"]) + "m",
                "actual": "$" + str(liquidity) + "m",
                "breach": True,
                "note": "Cash of $" + str(liquidity) + "m is below the $" + str(COVENANTS["min_liquidity_m"]) + "m minimum liquidity covenant."
            })

    coverage = metrics.get("interest_coverage_x")
    if coverage is not None:
        if coverage < COVENANTS["min_interest_coverage_x"]:
            breaches.append({
                "covenant": "Minimum Interest Coverage",
                "threshold": str(COVENANTS["min_interest_coverage_x"]) + "x",
                "actual": str(coverage) + "x",
                "breach": True,
                "note": "Interest coverage of " + str(coverage) + "x is below the " + str(COVENANTS["min_interest_coverage_x"]) + "x minimum threshold."
            })

    capex = metrics.get("capex_ytd_m")
    if capex is not None:
        if capex > COVENANTS["max_capex_ytd_m"]:
            breaches.append({
                "covenant": "Maximum Capex",
                "threshold": "$" + str(COVENANTS["max_capex_ytd_m"]) + "m",
                "actual": "$" + str(capex) + "m",
                "breach": True,
                "note": "YTD capex of $" + str(capex) + "m exceeds the $" + str(COVENANTS["max_capex_ytd_m"]) + "m annual limit."
            })

    return breaches, warnings

def print_report(filepath, metrics, breaches, warnings):
    print("=" * 60)
    print("COVENANT COMPLIANCE REPORT")
    print("File     : " + filepath)
    print("Borrower : " + str(metrics.get("borrower")))
    print("Period   : " + str(metrics.get("reporting_period")))
    print("Run at   : " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("=" * 60)
    print("\nEXTRACTED METRICS")
    print("  Adjusted EBITDA (LTM) : $" + str(metrics.get("adjusted_ebitda_ltm_m")) + "m")
    print("  Net Debt              : $" + str(metrics.get("net_debt_m")) + "m")
    print("  Leverage              : " + str(metrics.get("leverage_x")) + "x")
    print("  Interest Coverage     : " + str(metrics.get("interest_coverage_x")) + "x")
    print("  Cash                  : $" + str(metrics.get("cash_m")) + "m")
    print("  Capex YTD             : $" + str(metrics.get("capex_ytd_m")) + "m")
    print("  Add-backs             : $" + str(metrics.get("addbacks_m")) + "m")
    print("\nBORROWER STATEMENT")
    print("  " + str(metrics.get("borrower_compliance_statement")))

    if breaches:
        print("\nCOVENANT BREACHES DETECTED: " + str(len(breaches)))
        for b in breaches:
            print("\n  [" + b["covenant"] + "]")
            print("  Threshold : " + b["threshold"])
            print("  Actual    : " + b["actual"])
            print("  Note      : " + b["note"])
    else:
        print("\n  No covenant breaches detected.")

    if warnings:
        print("\nWARNINGS: " + str(len(warnings)))
        for w in warnings:
            print("\n  [" + w["covenant"] + "]")
            print("  Threshold : " + w["threshold"])
            print("  Actual    : " + w["actual"])
            print("  Note      : " + w["note"])

    print("\n" + "=" * 60)

def main():
    files = sys.argv[1:] if len(sys.argv) > 1 else [
        "borrower_update_clean.txt",
        "borrower_update_breach.txt"
    ]

    for filepath in files:
        print("\nProcessing " + filepath + "...")
        update_text = load_update(filepath)
        metrics = extract_metrics(update_text)
        breaches, warnings = run_covenant_checks(metrics)
        print_report(filepath, metrics, breaches, warnings)

        output_path = filepath.replace(".txt", "_result.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({"metrics": metrics, "breaches": breaches, "warnings": warnings}, f, indent=2)
        print("Result written to " + output_path)

if __name__ == "__main__":
    main()
