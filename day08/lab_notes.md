## Day 08 Lab Notes

Phase 8. Model benchmarking across eight models from three vendors, structured as a tier-based comparison: budget, mid and high capability. The objective was empirical comparison across a representative cross-section of the enterprise AI vendor landscape, not a superficial single-model-per-vendor exercise.

The benchmark ran the CIM triage workflow across Claude Haiku 4.5, Sonnet 4.6 and Opus 4.8 from Anthropic, GPT-4.1 mini, GPT-4.1 and o3 from OpenAI and Gemini 3.6 Flash and Gemini 3.1 Pro from Google. Three documents were processed: a borderline pass, a cleaner pass and a hard fail on dual sector exclusion.

The most analytically significant finding was on flag depth at the budget tier. GPT-4.1 mini returned zero flags on both passing deals while scoring them at 9. A model that scores correctly but surfaces no concerns is not useful in a credit workflow where the flags are the primary analytical output. Haiku and Gemini 3.6 Flash both returned two flags on the same documents at comparable scores, making them meaningfully more useful at equivalent cost and speed.

On mandate discipline, Sonnet 4.6 and Opus 4.8 scored the hard fail at 1, the most conservative result across all eight models. GPT-4.1 mini was the most lenient at 3. The remaining models clustered at 2. The Anthropic high-capability models are the most conservative on mandate discipline, which in a regulated credit context is a feature rather than a limitation.

Gemini 3.1 Pro was the slowest model tested, reaching 37 seconds on one document. GPT-4.1 was the fastest, averaging under 2 seconds. o3 produced substantially more output tokens than any other model, consistent with its reasoning-first architecture, and its response times reflected that. The additional token depth did not translate into materially different scores or flag counts on this task, suggesting that extended reasoning adds limited incremental value for structured extraction workflows of this type.

The tier-based structure of the benchmark makes the vendor comparison defensible. Comparing Haiku against GPT-4o, as the first version of this benchmark did, is not a like-for-like comparison. The revised design pairs models at equivalent capability and cost tiers, which produces findings that can be acted on rather than merely observed.

The README frames the benchmark as confirming Sonnet 4.6 was the right choice. The stronger framing is that it would have caught a wrong one. Cost and speed pull toward the budget tier. Only flag depth exposes it. The value of the lab is the detection capability, not the verdict.
