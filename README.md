# Private Credit Workflow Lab

A seven-day hands-on lab built in Python using the Anthropic API (claude-sonnet-4-6).

The lab simulates four core workflows from a private credit alternatives platform: deal triage, document ingestion, covenant compliance monitoring and LP portfolio reporting. It was built as a concrete technical artefact to accompany an executive job search targeting embedded AI product and platform roles in financial services.

## Structure

Each day is self-contained with its own scripts, sample documents and lab notes.

- **Day 01** - CIM triage: mandate-parameterised scoring of incoming deal documents
- **Day 02** - Ingestion loop: batch processing of multiple CIMs with CSV output and request logging
- **Day 03** - Covenant comparison: cross-document synthesis and deviation flagging
- **Day 04** - Compliance monitoring: financial extraction and covenant breach detection
- **Day 05** - LP reporting: narrative generation from structured portfolio data
- **Day 06** - Stress testing: edge cases, error handling and failure mode analysis
- **Day 07** - Synthesis: interview narrative and production gap assessment

## Stack

- Python 3.14
- Anthropic SDK 0.111.0
- Model: claude-sonnet-4-6
- Libraries: python-dotenv, csv, json

## Design principles

Prompts are structured to be declarative and mandate-specific, producing consistent and auditable outputs suitable for a regulated workflow context. Temperature is set to zero throughout to maximise predictability. Each script is self-contained and requires only a valid ANTHROPIC_API_KEY in a local .env file.

## Status

Days 01 and 02 complete.
