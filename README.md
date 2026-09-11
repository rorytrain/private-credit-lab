# Private Credit Workflow Lab

A hands-on lab built in Python across eight phases using the Anthropic, OpenAI and Google APIs.

The lab simulates four core workflows from a private credit alternatives platform, deal triage, document ingestion, covenant compliance monitoring and LP portfolio reporting, then tests the harness that runs them against seven further models from two other vendors. It was built to demonstrate applied AI prototyping capability in a private credit workflow context.

## Structure

Each day is self-contained with its own scripts, sample documents and lab notes.

- **Day 01** - CIM triage: mandate-parameterised scoring of incoming deal documents
- **Day 02** - Ingestion loop: batch processing of multiple CIMs with CSV output and request logging
- **Day 03** - Covenant comparison: cross-document synthesis and deviation flagging
- **Day 04** - Compliance monitoring: financial extraction and covenant breach detection
- **Day 05** - LP reporting: narrative generation from structured portfolio data
- **Day 06** - Stress testing: edge cases, error handling and failure mode analysis
- **Day 07** - Synthesis: build narrative, prompt engineering insight and production gap assessment. Originally scoped as the lab's endpoint.
- **Day 08** - Model benchmarking: the Day 07 conclusion, that the harness rather than the model was the durable asset, raised the question of whether that held across vendors. Day 08 tests it against seven further models.

## Architecture & Data Flow

```
Input Docs (CIMs / Credit Agreements / Financials)
└──> Declarative Prompt Engineering (Zero-Temperature)
     └──> Structured Extraction (JSON Outputs)
          └──> Rule Engine & Audit Logs (CSV / Verification)
               └──> LP Portfolio Summary Generation
                    └──> Model Benchmarking (Multi-Vendor Comparative Evaluation)
```

## Stack

- Python 3.14
- Anthropic SDK 0.111.0
- OpenAI SDK 3.11.0
- google-genai SDK 0.8.6
- Models: claude-haiku-4-5-20251001, claude-sonnet-4-6, claude-opus-4-8, gpt-4.1-mini, gpt-4.1, o3, gemini-3.6-flash, gemini-3.1-pro-preview
- Libraries: python-dotenv, csv, json


## Setup

Clone the repository and create a `.env` file in each day folder you intend to run.

Days 01 through 07 require only the Anthropic key:
```
ANTHROPIC_API_KEY=your-key-here
```

Day 08 requires all three vendor keys:
```
ANTHROPIC_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
GOOGLE_API_KEY=your-key-here
```

API keys are excluded from this repository by `.gitignore`. You will need API accounts with each vendor and sufficient credits. The lab was built and tested using the pay-as-you-go API tier across three vendors. Total API cost across all eight days is under USD 6, of which the majority is Anthropic usage across Days 01 through 07. Day 08 added OpenAI and Google API calls at negligible additional cost.

## Design principles

Prompts are structured to be declarative and mandate-specific, producing consistent and auditable outputs suitable for a regulated workflow context. Temperature is set to zero throughout to maximise predictability. Each script is self-contained and requires only the relevant vendor API keys in a local .env file.

## Status

All eight days complete. Days 01 through 07 complete the originally scoped lab; Day 08 extends it to test the harness against seven further models.

## Findings

The lab's central claim is that durable value in this kind of workflow sits in the harness rather than the model: the schema that enforces output structure, the validation layer that checks a model's claims rather than accepting them and the audit trail that makes a decision reviewable after the fact. Everything else in the lab, four private credit workflows and an eight-model benchmark across three vendors, exists to test that claim rather than assert it.

The clearest evidence for it is the CIM triage script's add-backs catch. The mandate parameters and output schema required the model to reconcile a leverage figure against defined thresholds rather than simply report one; against that requirement, it derived that one deal's management add-backs represented 28.7% of adjusted EBITDA, recomputed leverage on an unadjusted basis to 7.5x against a headline 5.8x and flagged the gap. Nothing in the source document stated that figure directly. The result isn't evidence of model reasoning, it's evidence that a harness built to demand reconciliation surfaces what a harness that only asks for a score would miss. The same pattern recurs across the lab: the covenant comparison script surfacing favourable deviations the schema required it to check for in both directions, not just one, the compliance monitor's prompt framing forcing a distinction between a clean confirmation and a hedge rather than accepting either as a pass, the LP reporting script's instruction against softening breaches producing a connection between an early triage flag and a later covenant breach that a neutral summary instruction would not have surfaced.

Temperature zero removes variance, it doesn't remove ambiguity. Where the prompt's mandate framing was precise, that determinism was an asset; the lab's own stress testing found the same zero-temperature setting reproducing an incorrect inference reliably once the framing left room for one. The harness's role is to hold the model to a defined standard regardless of which way temperature-zero happens to land, not to assume determinism is the same thing as correctness.

Day 08 exists to test that same principle under a variable the first seven phases held constant: the model itself. The finding is not which model scored best. It is that the harness caught a failure mode a scoreboard alone would have hidden: GPT-4.1 mini scored both passing deals correctly, a 9, and returned zero analytical flags on either, while Haiku 4.5 and Gemini 3.6 Flash, priced and positioned at the same tier, each returned two flags on the same documents at comparable scores. A model that scores correctly and surfaces nothing is not a cheaper version of a working tool, it is a different tool that happens to agree with the right answer on the documents it was shown, and the only reason that gap was visible at all is that the harness was built to check flag depth rather than accept a score on its own. Sonnet 4.6 and Opus 4.8 were, separately, the most conservative models tested on the hard-fail deal, scoring it 1 against a lenient 3 from GPT-4.1 mini. The benchmark's value was never confirming the right model had already been chosen. It was demonstrating that a harness built to interrogate rather than trust a model's output would have caught it if the wrong one had been.

The full reasoning is set out across two documents, deliberately kept separate rather than merged into one. [`day07/write_up.md`](day07/write_up.md) is the original synthesis, written at what was meant to be the lab's endpoint: the four workflows, the production gap and the harness conclusion above, reached before Day 08 existed. [`day08/write_up.md`](day08/write_up.md) carries that same document forward with a Phase 8 section added, the benchmark that followed from taking the Day 07 conclusion seriously enough to test it against seven other models. Read in order, the two show the reasoning happening rather than a finished argument presented after the fact. Day-by-day build notes sit alongside both, in each day's folder.

## Author

Rory Henry  
[linkedin.com/in/roryhenry](https://linkedin.com/in/roryhenry)
