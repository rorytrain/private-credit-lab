import os
import json
import time
from dotenv import load_dotenv
import anthropic
import openai
from google import genai as google_genai

load_dotenv()

anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
google_client = google_genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MANDATE = {
    "min_ebitda_m": 10,
    "max_ebitda_m": 75,
    "max_leverage": 5.0,
    "excluded_sectors": ["retail", "energy", "oil", "gas"],
    "preferred_structures": ["unitranche", "term loan", "senior secured"],
    "sponsor_backed_required": True
}

MODELS = [
    {"provider": "anthropic", "model": "claude-haiku-4-5-20251001", "label": "Claude Haiku 4.5"},
    {"provider": "anthropic", "model": "claude-sonnet-4-6", "label": "Claude Sonnet 4.6"},
    {"provider": "anthropic", "model": "claude-opus-4-8", "label": "Claude Opus 4.8"},
    {"provider": "openai", "model": "gpt-4o", "label": "GPT-4o"},
    {"provider": "google", "model": "gemini-3.1-pro-preview", "label": "Gemini 3.1 Pro"},
]

def load_cim(filepath):
    with open(filepath, "r") as f:
        return f.read()

def build_prompt(cim_text):
    return """You are a private credit analyst at a global alternatives platform.
Triage the following CIM against this mandate:
- EBITDA range: $""" + str(MANDATE["min_ebitda_m"]) + """m to $""" + str(MANDATE["max_ebitda_m"]) + """m
- Maximum leverage: """ + str(MANDATE["max_leverage"]) + """x
- Excluded sectors: """ + ", ".join(MANDATE["excluded_sectors"]) + """
- Preferred structures: """ + ", ".join(MANDATE["preferred_structures"]) + """
- Sponsor-backed deals only

Return only a JSON object with this exact structure and no other text:
{
    "company_name": "",
    "sponsor": "",
    "sector": "",
    "adjusted_ebitda_m": 0,
    "facility_m": 0,
    "leverage_x": 0,
    "structure": "",
    "mandate_fit_score": 0,
    "mandate_fit_rationale": "",
    "flags": []
}

Mandate fit score: 1 to 10 where 10 is a perfect fit.
Flags: a list of strings each no more than two sentences.
Be concise. Return only the JSON object.

CIM TEXT:
""" + cim_text

def call_anthropic(model, prompt):
    start = time.time()
    try:
        kwargs = {
            "model": model,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }
        if "opus" not in model.lower():
            kwargs["temperature"] = 0
        response = anthropic_client.messages.create(**kwargs)
        elapsed = round(time.time() - start, 2)
        raw = response.content[0].text
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        return raw, input_tokens, output_tokens, elapsed, None
    except Exception as e:
        return None, 0, 0, 0, str(e)

def call_openai(model, prompt):
    start = time.time()
    try:
        response = openai_client.chat.completions.create(
            model=model,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        elapsed = round(time.time() - start, 2)
        raw = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        return raw, input_tokens, output_tokens, elapsed, None
    except Exception as e:
        return None, 0, 0, 0, str(e)

def call_google(model, prompt):
    start = time.time()
    try:
        response = google_client.models.generate_content(
            model=model,
            contents=prompt
        )
        elapsed = round(time.time() - start, 2)
        raw = response.text
        input_tokens = response.usage_metadata.prompt_token_count
        output_tokens = response.usage_metadata.candidates_token_count
        return raw, input_tokens, output_tokens, elapsed, None
    except Exception as e:
        return None, 0, 0, 0, str(e)

def parse_json(raw):
    try:
        clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(clean), None
    except Exception as e:
        return None, str(e)

def run_benchmark(cim_filepath):
    cim_text = load_cim(cim_filepath)
    prompt = build_prompt(cim_text)
    results = []

    print("\nBenchmarking: " + cim_filepath)
    print("-" * 60)

    for m in MODELS:
        print("  Running " + m["label"] + "...")

        if m["provider"] == "anthropic":
            raw, input_tokens, output_tokens, elapsed, error = call_anthropic(m["model"], prompt)
        elif m["provider"] == "openai":
            raw, input_tokens, output_tokens, elapsed, error = call_openai(m["model"], prompt)
        else:
            raw, input_tokens, output_tokens, elapsed, error = call_google(m["model"], prompt)

        if error:
            print("    ERROR: " + error)
            results.append({
                "model": m["label"],
                "error": error
            })
            continue

        result, parse_error = parse_json(raw)

        if parse_error:
            print("    PARSE ERROR: " + parse_error)
            results.append({
                "model": m["label"],
                "parse_error": parse_error,
                "raw": raw[:200]
            })
            continue

        entry = {
            "model": m["label"],
            "mandate_fit_score": result.get("mandate_fit_score"),
            "company_name": result.get("company_name"),
            "sector": result.get("sector"),
            "adjusted_ebitda_m": result.get("adjusted_ebitda_m"),
            "leverage_x": result.get("leverage_x"),
            "flag_count": len(result.get("flags", [])),
            "flags": result.get("flags", []),
            "rationale": result.get("mandate_fit_rationale"),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "elapsed_seconds": elapsed
        }

        results.append(entry)

        print("    Score: " + str(entry["mandate_fit_score"]) +
              " | Flags: " + str(entry["flag_count"]) +
              " | Tokens in/out: " + str(input_tokens) + "/" + str(output_tokens) +
              " | Time: " + str(elapsed) + "s")

    return results

def print_comparison(all_results):
    print("\n" + "=" * 60)
    print("BENCHMARK COMPARISON SUMMARY")
    print("=" * 60)

    for filepath, results in all_results.items():
        print("\nDocument: " + filepath)
        print("{:<20} {:>6} {:>6} {:>8} {:>8} {:>8}".format(
            "Model", "Score", "Flags", "In Tok", "Out Tok", "Secs"))
        print("-" * 60)
        for r in results:
            if "error" in r or "parse_error" in r:
                print("{:<20} {:>6}".format(r["model"], "ERROR"))
            else:
                print("{:<20} {:>6} {:>6} {:>8} {:>8} {:>8}".format(
                    r["model"],
                    str(r["mandate_fit_score"]),
                    str(r["flag_count"]),
                    str(r["input_tokens"]),
                    str(r["output_tokens"]),
                    str(r["elapsed_seconds"])
                ))

def main():
    cim_files = [
        "sample_cim.txt",
        "sample_cim_2.txt",
        "sample_cim_3.txt"
    ]

    all_results = {}

    for filepath in cim_files:
        results = run_benchmark(filepath)
        all_results[filepath] = results

    print_comparison(all_results)

    output_path = "benchmark_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)

    print("\nFull results written to " + output_path)

if __name__ == "__main__":
    main()
