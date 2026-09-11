# Private Credit Workflow Lab
*Synthesis Document*

*Rory Henry · September 2026*

---

## What Was Built and How

This lab was built collaboratively with Claude, Anthropic's AI assistant, across eight phases of work. Each phase, or 'day', represents a distinct unit of delivery, some completed in a single session and others developed across multiple sessions over several days. The phases are numbered for structure, not to imply a fixed daily cadence.

Day 7 was the intended endpoint. Four workflows had been built and stress tested, and the synthesis phase existed to draw that work together into a single account. What that phase actually confirmed, though, was that the harness, not the model, was the load-bearing part of the build: the schema enforcement, the validation layer, the audit logging. A harness built to that standard raised an obvious question the lab hadn't yet answered, whether the analytical results were a property of Claude specifically or of the harness design generally. Day 8 exists to answer that question, and is best read as a consequence of Day 7's conclusion rather than an extension of scope.

The architecture, analytical framework and mandate parameters were developed through iterative dialogue with Claude, with the domain knowledge and critical direction coming from the practitioner side of the conversation. Claude generated code, produced sample documents and drafted outputs. Where the model produced plausible but incorrect results, they were caught and corrected. Where the analytical output was strong, it was recognised, extended and pushed further. The collaboration worked as an augmentation of critical thinking rather than a delegation of it. The outcomes are more qualitative and more precise as a result of that interaction than either party would have produced working independently.

The lab simulates four core workflows from an institutional private credit platform, built on the Anthropic API and Claude Sonnet 4.6, and then tests the harness that runs them against seven further models from two other vendors. It runs from the command line, processes unstructured financial documents and produces structured, auditable outputs at each stage. The repository is at github.com/rorytrain/private-credit-lab.

---

## The Four Workflow Simulations

*Deal Triage.* A CIM is read as plain text, assembled into a structured prompt alongside a defined mandate profile and scored for mandate fit. The output is a JSON object containing extracted financial parameters, a score from 1 to 10 and a set of analytical flags. Validated against three deals spanning a borderline pass, a cleaner pass and a hard fail on dual sector exclusion. The script correctly derived that one deal's management add-backs represented 28.7% of adjusted EBITDA, recomputed leverage on an unadjusted basis at 7.5x and flagged the gap without being explicitly instructed to do so.

*Document Ingestion.* The triage script was extended into a batch loop processing multiple CIMs in sequence, writing one row per document to a CSV and logging each full request and response pair to a text file. Temperature zero was introduced here, making the pipeline behave more like a deterministic rule engine than a generative system.

*Covenant Comparison.* Two credit agreements were fed to Claude simultaneously. The model extracted covenant terms from both, compared them against a set of internal threshold parameters defined in code and returned a deviations array with severity ratings. The script identified six high-severity deviations in one agreement and correctly treated deviation as bidirectional, surfacing favourable deviations in the compliant agreement without being asked. In a production context those parameters would be governed by a formal credit policy document rather than a script-level dictionary, but the analytical logic and deviation detection are structurally sound.

*Covenant Compliance Monitoring.* A borrower sends a monthly financial update. Claude extracts the key metrics. A Python validation layer checks those metrics against defined covenant thresholds and fires breach alerts. The most analytically significant output was the borrower compliance statement: the model distinguished between a borrower explicitly confirming compliance and a borrower hedging about covenant pressure, without being instructed to look for that difference.

*Limited Partner (LP) Portfolio Reporting.* Structured outputs from the preceding phases were compiled into a portfolio data pack and Claude was instructed to draft a quarterly LP update. The prompt required candour and prohibited softening of covenant breaches. The output named all four Project Apex breaches directly, quantified the EBITDA deterioration at 18% and noted that the origination triage flags had proven material, synthesising phases 1 and 4 without being instructed to make the connection.

---

## The Most Important Prompt Engineering Insight

Role framing and explicit behavioural constraints shape not just the format of the output but the analytical lens the model (Sonnet 4.6) applies. Telling the model it is a credit analyst rather than a data extractor produces materially different output from the same document. Telling it not to soften covenant breaches produces a document that reads like it was written by someone who respects their LP's intelligence.

Temperature zero makes the model predictable but does not make it correct. If the prompt is ambiguous, the model will predictably misinterpret it every time. Phase 6 stress testing demonstrated this directly: the covenant extraction prompt produced inconsistent results across runs at temperature zero when the framing left room for the model to infer covenant existence from a reference to an absent document. Prompt precision is the primary engineering lever. Temperature is a secondary constraint that reduces variance around whatever direction the prompt establishes.

---

## The Production Gap

The prototype demonstrates that the workflow logic is sound and that Claude can perform these analytical tasks reliably when the prompt is well-constructed. The gap between prototype and production is specific and worth naming:

- Each script processes one document at a time with no awareness of portfolio context. A production system requires an orchestration layer that aggregates subagent outputs and applies portfolio-level judgment. Every output must carry its provenance: what was checked, by what method and against what source, not just its content. That orchestrator must treat subagent outputs as evidence to be interrogated rather than fact to be accepted. A failure mode was demonstrated directly during the build when a claim generated in one conversation session was carried into another and nearly acted on without independent verification. In a multi-agent system that dynamic compounds silently across every hop.

- The compliance monitoring phase revealed that the model extracts a single leverage figure from contradictory inputs and tends toward the more favourable number. Source data provenance controls and auditor sign-off are required before figures enter the compliance pipeline. Prompting can flag the conflict. It cannot resolve it.

- The covenant comparison phase revealed that the model sets a covenants_found flag based on references to documents it has not seen. Document completeness validation is required before extraction runs.

- Secrets management is not a prompt engineering problem. Static API keys in environment files require rotation discipline and process controls. During the build the .gitignore was lost during a history rewrite and two live keys were committed to version control before GitHub's push protection intercepted them. Identity federation, short-lived tokens issued by a cloud provider, is the production answer. Anthropic now supports it.

- The audit trail in this prototype is a text log. A production system requires immutable, timestamped, tamper-evident logging with retention policies aligned to regulatory requirements.

---

## Phase 8: Testing the Harness Against the Model

The first seven phases answered whether Claude could perform private credit analytical tasks reliably. They did not answer a separate question the harness itself had made askable: whether the results were a property of Sonnet 4.6 specifically, or a property of the harness design, in which case the same schema and validation logic should produce comparable analytical discipline from a different model underneath it. Phase 8 tested that directly, running the triage workflow unchanged against eight models across three vendors, Claude Haiku 4.5, Sonnet 4.6 and Opus 4.8, GPT-4.1 mini, GPT-4.1 and o3, and Gemini 3.6 Flash and Gemini 3.1 Pro, grouped into budget, mid and high capability tiers so that comparisons held cost and capability roughly constant rather than comparing a budget model to a flagship.

The result that mattered most sat at the budget tier and would not have been visible from score alone. GPT-4.1 mini scored both passing deals correctly, a 9, but returned zero analytical flags on either document. Haiku 4.5 and Gemini 3.6 Flash, priced and positioned comparably, each returned two flags on the same documents at equivalent scores. A model that scores correctly but surfaces nothing is not a cheaper version of a working triage tool, it is a different tool that happens to agree with the right answer on the documents it was shown. In a workflow where the flags are the analytical product and the score is a summary of them, that distinction is the whole finding.

On mandate discipline, the two Anthropic high-capability models, Sonnet 4.6 and Opus 4.8, scored the hard-fail deal at 1, the most conservative result of the eight. GPT-4.1 mini scored it a 3. The remaining five models clustered at 2. Latency and token behaviour varied on their own axis and did not track with analytical quality: Gemini 3.1 Pro was the slowest model tested at 37 seconds against GPT-4.1's sub-2-second average, and o3 produced markedly more output tokens than any other model without a corresponding gain in flag depth or score accuracy, consistent with reasoning overhead that this kind of structured extraction task does not need.

The honest framing of Phase 8 is not that it confirmed Sonnet 4.6 was the right choice, though it did. It is that the benchmark would have caught a wrong one. Cost and latency pull toward the budget tier on their own; nothing about GPT-4.1 mini's speed or price would have signalled the problem. Only flag depth exposed it, and flag depth is only visible if something is built to check for it. That is the actual conclusion of the lab: the harness is not a wrapper around a chosen model, it is the thing that makes model choice, and model substitution, a governable decision rather than a vendor commitment taken on faith.
