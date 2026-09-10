# Private Credit Workflow Lab

A hands-on lab built in Python across eight phases using the Anthropic API (claude-sonnet-4-6).

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
- Models: claude-haiku-4-5-20251001, claude-sonnet-4-6, claude-opus-4-8, gpt-4o, gemini-3.1-pro-preview
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

## Footnote

The Private Credit Workflow Lab is a Python prototype built across eight phases ('days') that simulates four core workflows from an institutional private credit platform: deal triage, document ingestion, covenant comparison and compliance monitoring. Each workflow takes unstructured financial documents (CIMs, credit agreements and borrower updates) and uses Claude Sonnet 4.6 via the Anthropic API to extract structured data, apply analytical judgment and produce auditable outputs. The architecture is deliberately simple: declarative prompts at zero temperature, JSON extraction, Python rule engines and file-based logging. The simplicity is intentional; it demonstrates that meaningful workflow automation does not require complex infrastructure, but instead leans heavily on precise prompt design and a well-defined data contract.

The business value being demonstrated is the automation of cognitive workflows that currently consume significant analyst time in private credit operations. A junior analyst reading a CIM to assess mandate fit, a credit officer cross-referencing two credit agreements for covenant deviations, a portfolio manager checking monthly borrower updates for covenant breaches. Each of these tasks involves reading unstructured documents, applying domain-specific judgment and producing a structured output. The lab shows that Claude can perform all three steps reliably when the prompt is framed with sufficient domain specificity. The triage script scores deals against a defined mandate. The covenant comparison script identifies deviations with severity ratings. The compliance monitor distinguishes between a borrower confirming compliance and a borrower hedging. None of that analytical output was explicitly programmed, it emerged from role framing and prompt precision.

The deeper insight the lab surfaces is about the nature of the harness rather than the model. The model is text in, text out: stateless, context-bound and only as analytically precise as the prompt that frames it. What the lab actually builds is a lightweight harness: context management, output parsing, rule validation, error handling and audit logging. That distinction matters for the production gap conversation on Days 06 and 07 and it maps directly to the broader industry debate about where agentic AI creates durable enterprise value.

The lab is a concrete, working instance of the argument that the most immediate ROI from generative AI in financial services is not model sophistication but workflow integration: replacing the unstructured cognitive labour that sits between data ingestion and decision output.

Day 08 extended the lab into model benchmarking, running the same CIM triage workflow across five models from three vendors: Claude Haiku 4.5, Claude Sonnet 4.6 and Claude Opus 4.8 from Anthropic, GPT-4o from OpenAI and Gemini 3.1 Pro from Google. The benchmark measured mandate fit score, flag depth, token consumption and response latency across three deals spanning a borderline pass, a cleaner pass and a hard fail.

The most significant finding was on mandate discipline. On the hard fail deal, Opus 4.8 scored it 1, Sonnet 4.6, Gemini 3.1 Pro and Haiku all scored it 2 and GPT-4o scored it 3. GPT-4o was the most lenient on a deal that should be declined outright. On the borderline pass, GPT-4o returned a score of 10 with zero flags while Sonnet returned 8 with four flags. In a regulated credit context, a model that passes deals cleanly without surfacing concerns is a liability rather than an asset.

Sonnet 4.6 produced the most flags and the most conservative scores consistently across all three deals. For a private credit triage workflow where analytical depth and mandate discipline matter more than speed or cost, Sonnet is the right model. Haiku and GPT-4o are competitive for high-volume first-pass filtering where latency and cost are the primary constraints. Gemini 3.1 Pro was the slowest model tested, averaging 15 seconds per call compared to an average of 4 seconds across the other four models.
