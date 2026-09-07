import os
import json
import sys
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MANDATE = {
    "min_ebitda_m": 10,
    "max_ebitda_m": 75,
    "max_leverage": 5.0,
    "excluded_sectors": ["retail", "energy", "oil", "gas"],
    "preferred_structures": ["unitranche", "term loan", "senior secured"],
    "sponsor_backed_required": True
}

COVENANTS = {
    "max_leverage_x": 4.25,
    "min_liquidity_m": 3.0,
    "max_capex_ytd_m": 4.0,
    "min_interest_coverage_x": 3.0
}

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

def load_file(filepath):
    with open(filepath, "r") as f:
        return f.read()

def call_claude(prompt, max_tokens=4096):
    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=max_tokens,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text, None
    except Exception as e:
        return None, str(e)

def parse_json_response(raw):
    try:
        clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(clean), None
    except json.JSONDecodeError as e:
        # Attempt to recover a partial object by finding the last complete field
        try:
            truncated = clean[:clean.rfind("}")]
            if truncated:
                truncated = truncated + "}" * (clean.count("{") - clean.count("}") + 1)
                return json.loads(truncated), "PARTIAL PARSE: response was truncated"
        except Exception:
            pass
        return None, "PARSE FAILED: " + str(e)

def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def print_result(label, value, warning=False):
    prefix = "  WARNING:" if warning else "  "
    print(prefix + " " + label + ": " + str(value))

def stress_test_triage(filepath):
    print_section("PHASE 1 STRESS TEST: CIM TRIAGE")
    print("  Input: " + filepath)

    text = load_file(filepath)
    prompt = """You are a private credit analyst at a global alternatives platform.
Triage the following CIM against this mandate:
- EBITDA range: $10m to $75m
- Maximum leverage: 5.0x
- Excluded sectors: retail, energy, oil, gas
- Preferred structures: unitranche, term loan, senior secured
- Sponsor-backed deals only

Return a JSON object with this exact structure:
{
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
    "flags": [],
    "data_quality_issues": []
}

Use null for any field not present in the document.
Add a data_quality_issues array listing any missing or ambiguous fields.
Mandate fit score: 1 to 10. Score must reflect data quality — missing critical
fields should materially reduce the score.
Flags and data_quality_issues: no more than two sentences each.

CIM TEXT:
""" + text

    raw, api_error = call_claude(prompt)

    if api_error:
        print("  API ERROR: " + api_error)
        return

    result, parse_error = parse_json_response(raw)

    if parse_error:
        print("  PARSE ERROR: " + parse_error)
        print("  RAW RESPONSE: " + raw[:2000])
        return

    print_result("Company", result.get("company_name"))
    print_result("Mandate Fit Score", result.get("mandate_fit_score"))
    print_result("EBITDA", result.get("adjusted_ebitda_m"))
    print_result("Facility", result.get("facility_m"))

    issues = result.get("data_quality_issues", [])
    if issues:
        print("\n  DATA QUALITY ISSUES DETECTED: " + str(len(issues)))
        for issue in issues:
            print("    - " + issue)
    else:
        print("\n  No data quality issues detected.")

    flags = result.get("flags", [])
    if flags:
        print("\n  FLAGS: " + str(len(flags)))
        for flag in flags:
            print("    - " + flag)

    print("\n  FAILURE MODE OBSERVED:")
    if result.get("adjusted_ebitda_m") is None and result.get("facility_m") is None:
        print("  Model returned nulls for critical fields. Score reflects uncertainty.")
        print("  A production system requires a minimum data threshold before scoring.")
    else:
        print("  Model attempted to score despite missing data. Verify score reliability.")

def stress_test_compliance(filepath):
    print_section("PHASE 2 STRESS TEST: COMPLIANCE MONITOR")
    print("  Input: " + filepath)

    text = load_file(filepath)
    prompt = """You are a credit monitoring analyst.
Extract the following financial metrics from the borrower update below.
Return only a JSON object with this exact structure and no other text:
{
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
    "borrower_compliance_statement": "",
    "data_quality_issues": [],
    "conflicting_figures": []
}

Use null for any field not present.
List any contradictory or ambiguous figures in conflicting_figures.
The borrower_compliance_statement should be a one-sentence summary.

BORROWER UPDATE:
""" + text

    raw, api_error = call_claude(prompt)

    if api_error:
        print("  API ERROR: " + api_error)
        return

    result, parse_error = parse_json_response(raw)

    if parse_error:
        print("  PARSE ERROR: " + parse_error)
        print("  RAW RESPONSE: " + raw[:500])
        return

    print_result("Borrower", result.get("borrower"))
    print_result("Leverage extracted", result.get("leverage_x"))
    print_result("Cash extracted", result.get("cash_m"))

    conflicts = result.get("conflicting_figures", [])
    if conflicts:
        print("\n  CONFLICTING FIGURES DETECTED: " + str(len(conflicts)), True)
        for c in conflicts:
            print("    - " + c)
    else:
        print("\n  No conflicting figures detected.")

    issues = result.get("data_quality_issues", [])
    if issues:
        print("\n  DATA QUALITY ISSUES: " + str(len(issues)))
        for issue in issues:
            print("    - " + issue)

    print("\n  FAILURE MODE OBSERVED:")
    leverage = result.get("leverage_x")
    if leverage is not None:
        print("  Model extracted a leverage figure from contradictory inputs.")
        print("  Which figure did it use? Management accounts (3.2x) or audited (4.9x)?")
        print("  Extracted value: " + str(leverage) + "x")
        if leverage < 4.25:
            print("  RISK: Compliance check would PASS on this figure.")
            print("  A production system must not accept unaudited figures for covenant testing.")
        else:
            print("  Model used the more conservative audited figure.")

def stress_test_covenant(filepath):
    print_section("PHASE 3 STRESS TEST: COVENANT COMPARISON")
    print("  Input: " + filepath)

    text = load_file(filepath)
    prompt = """You are a senior credit analyst.
Review the following credit agreement and extract all financial covenant terms.
Return a JSON object with this exact structure:
{
    "borrower": "",
    "facility_m": 0,
    "covenants_found": true,
    "covenants": {
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
    },
    "data_quality_issues": [],
    "extraction_confidence": ""
}

Set covenants_found to false if no covenant terms are present.
Use null for any covenant not specified.
extraction_confidence must be one of: HIGH, MEDIUM, LOW, NONE.
data_quality_issues: list any missing, redacted or externally referenced terms.
Be concise. Return only the JSON object with no preamble, explanation or trailing text.

CREDIT AGREEMENT:
""" + text

    raw, api_error = call_claude(prompt)

    if raw:
        print("  Raw response length: " + str(len(raw)) + " characters")

    if api_error:
        print("  API ERROR: " + api_error)
        return

    result, parse_error = parse_json_response(raw)

    if parse_error:
        print("  PARSE ERROR: " + parse_error)
        print("  RAW RESPONSE: " + raw[:500])
        return

    print_result("Borrower", result.get("borrower"))
    print_result("Covenants found", result.get("covenants_found"))
    print_result("Extraction confidence", result.get("extraction_confidence"))

    issues = result.get("data_quality_issues", [])
    if issues:
        print("\n  DATA QUALITY ISSUES: " + str(len(issues)))
        for issue in issues:
            print("    - " + issue)

    print("\n  FAILURE MODE OBSERVED:")
    covenants_found = result.get("covenants_found")
    covenants = result.get("covenants", {})
    all_null = all(v is None for v in covenants.values()) if covenants else True

    if covenants_found and all_null:
        print("  CRITICAL: Model set covenants_found=true but all covenant values are null.")
        print("  A downstream process reading covenants_found=true would proceed incorrectly.")
        print("  Production requirement: validate covenant completeness, not just presence flag.")
    elif not covenants_found:
        print("  Model correctly identified that covenant terms are absent.")
        print("  A production system must halt and escalate when covenant data is missing.")
    else:
        print("  Model attempted extraction despite redacted terms. Review confidence rating.")

def main():
    print("\nDAY 06 STRESS TEST RUNNER")
    print("Private Credit Workflow Lab")
    print("Testing failure modes across all three analytical phases\n")

    stress_test_triage("stress_cim_incomplete.txt")
    stress_test_compliance("stress_borrower_ambiguous.txt")
    stress_test_covenant("stress_agreement_empty.txt")

    print_section("SUMMARY: FAILURE MODES THAT PROMPTING CANNOT SOLVE")
    print("""
  PHASE 1 — CIM TRIAGE
  Failure mode: Model will score a deal even when critical fields are absent.
  What prompting can do: instruct the model to flag missing data and reduce score.
  What prompting cannot do: enforce a minimum data threshold before scoring runs.
  Production requirement: a data validation gate before the prompt is assembled.

  PHASE 2 — COMPLIANCE MONITORING
  Failure mode: Model may extract a single leverage figure from contradictory inputs.
  What prompting can do: instruct the model to flag conflicting figures.
  What prompting cannot do: determine which figure is authoritative.
  Production requirement: source data provenance controls and auditor sign-off
  before figures enter the compliance pipeline.

  PHASE 3 — COVENANT COMPARISON
  Failure mode: Model cannot extract covenants from a side letter it has not seen.
  What prompting can do: instruct the model to flag missing documents.
  What prompting cannot do: retrieve the side letter or reason about its contents.
  Production requirement: document completeness check before extraction runs.
  All referenced documents must be present in the input package.

  CROSS-CUTTING FAILURE MODES
  1. Secrets management: static API keys in environment files require rotation
     discipline and process controls. Identity federation is the production answer.
  2. Orchestrator trust: in a multi-agent system, subagent outputs must carry
     their verification status, not just their content. An orchestrator that treats
     triage scores as indisputable fact compounds errors silently.
  3. Audit trail: the requests_log.txt in Day 02 is a prototype audit log.
     A production system requires immutable, timestamped, tamper-evident logging
     with retention policies aligned to regulatory requirements.
""")

if __name__ == "__main__":
    main()
