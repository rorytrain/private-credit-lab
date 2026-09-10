# Private Credit Workflow Lab

A hands-on lab built in Python across eight phases using the Anthropic, OpenAI and Google APIs.

The lab simulates four core workflows from a private credit alternatives platform: deal triage, document ingestion, covenant compliance monitoring and LP portfolio reporting. It was built to demonstrate applied AI prototyping capability in a private credit workflow context.

## Structure

Each day is self-contained with its own scripts, sample documents and lab notes.

- **Day 01** - CIM triage: mandate-parameterised scoring of incoming deal documents
- **Day 02** - Ingestion loop: batch processing of multiple CIMs with CSV output and request logging
- **Day 03** - Covenant comparison: cross-document synthesis and deviation flagging
- **Day 04** - Compliance monitoring: financial extraction and covenant breach detection
- **Day 05** - LP reporting: narrative generation from structured portfolio data
- **Day 06** - Stress testing: edge cases, error handling and failure mode analysis
- **Day 07** - Synthesis: build narrative, prompt engineering insight and production gap assessment
- **Day 08** - Model benchmarking: same workflows run against multiple models for comparative evaluation

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

All eight days complete.

## Findings

The Private Credit Workflow Lab is a Python prototype built across eight phases ('days') that simulates four core workflows from an institutional private credit platform: deal triage, document ingestion, covenant comparison and compliance monitoring. Each workflow takes unstructured financial documents (CIMs, credit agreements and borrower updates) and uses Claude Sonnet 4.6 via the Anthropic API to extract structured data, apply analytical judgment and produce auditable outputs. The architecture is deliberately simple: declarative prompts at zero temperature, JSON extraction, Python rule engines and file-based logging. The simplicity is intentional; it demonstrates that meaningful workflow automation does not require complex infrastructure, but instead leans heavily on precise prompt design and a well-defined data contract.

The business value being demonstrated is the automation of cognitive workflows that currently consume significant analyst time in private credit operations. A junior analyst reading a CIM to assess mandate fit, a credit officer cross-referencing two credit agreements for covenant deviations, a portfolio manager checking monthly borrower updates for covenant breaches. Each of these tasks involves reading unstructured documents, applying domain-specific judgment and producing a structured output. The lab shows that Claude can perform all three steps reliably when the prompt is framed with sufficient domain specificity. The triage script scores deals against a defined mandate. The covenant comparison script identifies deviations with severity ratings. The compliance monitor distinguishes between a borrower confirming compliance and a borrower hedging. None of that analytical output was explicitly programmed, it emerged from role framing and prompt precision.

The deeper insight the lab surfaces is about the nature of the harness rather than the model. The model is text in, text out: stateless, context-bound and only as analytically precise as the prompt that frames it. What the lab actually builds is a lightweight harness: context management, output parsing, rule validation, error handling and audit logging. That distinction matters for the production gap conversation on Days 06 and 07 and it maps directly to the broader industry debate about where agentic AI creates durable enterprise value.

The lab is a concrete, working instance of the argument that the most immediate ROI from generative AI in financial services is not model sophistication but workflow integration: replacing the unstructured cognitive labour that sits between data ingestion and decision output.

Day 08 extended the lab into model benchmarking, structured as a tier-based comparison across eight models from three vendors: Claude Haiku 4.5, Sonnet 4.6 and Opus 4.8 from Anthropic, GPT-4.1 mini, GPT-4.1 and o3 from OpenAI and Gemini 3.6 Flash and Gemini 3.1 Pro from Google. The benchmark measured mandate fit score, flag depth, token consumption and response latency across three deals spanning a borderline pass, a cleaner pass and a hard fail. The tier-based design pairs models at equivalent capability and cost points across vendors, producing findings that are analytically defensible rather than superficially comparative.

The most significant finding was on flag depth at the budget tier. GPT-4.1 mini returned zero flags on both passing deals while scoring them at 9. A model that scores correctly but surfaces no concerns is not useful in a credit workflow where the flags are the primary analytical output. Haiku and Gemini 3.6 Flash both returned two flags on the same documents at comparable scores, making them meaningfully more useful for triage at equivalent cost and speed. On mandate discipline, Sonnet 4.6 and Opus 4.8 scored the hard fail at 1, the most conservative result across all eight models. GPT-4.1 mini was the most lenient at 3. The remaining models clustered at 2.

Gemini 3.1 Pro was the slowest model tested, reaching 37 seconds on one document against a GPT-4.1 average of under 2 seconds. o3 produced substantially more output tokens than any other model, consistent with its reasoning-first architecture, but the additional depth did not translate into materially different scores or flag counts on structured extraction tasks of this type. For a private credit triage workflow where analytical conservatism and flag depth matter more than speed or cost, Sonnet 4.6 remains the right model.

The more precise observation is that the benchmark would have caught a wrong choice. Cost and speed pull naturally toward the budget tier. Only flag depth exposes the risk of making that move. The value of the exercise is the detection capability, not the verdict.

The benchmark surfaces a broader architectural principle. Models are replaceable compute. The durable value sits in the surrounding harness: schema enforcement, audit logging and exception routing, none of which are model-dependent. A vendor switch changes the API call. It does not change the workflow.
