# Private Credit Workflow Lab

A seven-day hands-on lab built in Python using the Anthropic API (claude-sonnet-4-6).

The lab simulates four core workflows from a private credit alternatives platform: deal triage, document ingestion, covenant compliance monitoring and LP portfolio reporting. It was built to demonstrate applied AI prototyping capability in a private credit workflow context.

## Structure

Each day is self-contained with its own scripts, sample documents and lab notes.

- **Day 01** - CIM triage: mandate-parameterised scoring of incoming deal documents
- **Day 02** - Ingestion loop: batch processing of multiple CIMs with CSV output and request logging
- **Day 03** - Covenant comparison: cross-document synthesis and deviation flagging
- **Day 04** - Compliance monitoring: financial extraction and covenant breach detection
- **Day 05** - LP reporting: narrative generation from structured portfolio data
- **Day 06** - Stress testing: edge cases, error handling and failure mode analysis
- **Day 07** - Synthesis: interview narrative and production gap assessment

## Architecture & Data Flow

```
Input Docs (CIMs / Credit Agreements / Financials)
└──> Declarative Prompt Engineering (Zero-Temperature)
     └──> Structured Extraction (JSON Outputs)
          └──> Rule Engine & Audit Logs (CSV / Verification)
               └──> LP Portfolio Summary Generation
```

## Stack

- Python 3.14
- Anthropic SDK 0.111.0
- Model: claude-sonnet-4-6
- Libraries: python-dotenv, csv, json


## Setup

Clone the repository and create a `.env` file in each day folder you intend to run: ANTHROPIC_API_KEY=your-key-here

API keys are excluded from this repository by `.gitignore`. You will need an Anthropic API account with sufficient credits. The lab was built and tested using the pay-as-you-go API tier — total cost for all seven days is under USD 5.

## Design principles

Prompts are structured to be declarative and mandate-specific, producing consistent and auditable outputs suitable for a regulated workflow context. Temperature is set to zero throughout to maximise predictability. Each script is self-contained and requires only a valid ANTHROPIC_API_KEY in a local .env file.

## Status

Days 01 to 03 complete.

## Footnote

The Private Credit Workflow Lab is a seven-day Python prototype that simulates four core workflows from an institutional private credit platform: deal triage, document ingestion, covenant comparison and compliance monitoring. Each workflow takes unstructured financial documents — CIMs, credit agreements and borrower updates — and uses Claude Sonnet 4.6 via the Anthropic API to extract structured data, apply analytical judgment and produce auditable outputs. The architecture is deliberately simple: declarative prompts at zero temperature, JSON extraction, Python rule engines and file-based logging. The simplicity is intentional — it demonstrates that meaningful workflow automation does not require complex infrastructure, only precise prompt design and a well-defined data contract.

The business value being demonstrated is the automation of cognitive workflows that currently consume significant analyst time in private credit operations. A junior analyst reading a CIM to assess mandate fit, a credit officer cross-referencing two credit agreements for covenant deviations, a portfolio manager checking monthly borrower updates for covenant breaches — each of these tasks involves reading unstructured documents, applying domain-specific judgment and producing a structured output. The lab shows that Claude can perform all three steps reliably when the prompt is framed with sufficient domain specificity. The triage script scores deals against a defined mandate. The covenant comparison script identifies deviations with severity ratings. The compliance monitor distinguishes between a borrower confirming compliance and a borrower hedging. None of that analytical output was explicitly programmed — it emerged from role framing and prompt precision.

The deeper insight the lab surfaces is about the nature of the harness rather than the model. The model is text in, text out — stateless, context-bound and only as analytically precise as the prompt that frames it. What the lab actually builds is a lightweight harness: context management, output parsing, rule validation, error handling and audit logging. That distinction matters for the production gap conversation on Day 6 and Day 7, and it maps directly to the broader industry debate about where agentic AI creates durable enterprise value. The lab is a concrete, working instance of the argument that the most immediate ROI from generative AI in financial services is not model sophistication but workflow integration — replacing the unstructured cognitive labour that sits between data ingestion and decision output.