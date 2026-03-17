# RevenueCat Growth Brief — Process Log

## Objective
Build a useful public tool/resource on top of RevenueCat's Charts API, then package it with launch content and a growth campaign to drive awareness and adoption among AI agent developers and growth communities.

## Timeline
- Assignment received: March 16, 2026
- 48-hour window from receipt

## Phase 1 — Research & strategy (hours 0–2)

### API exploration
1. Validated the provided API key against RevenueCat API v2.
2. Confirmed Dark Noise project access (`proj058a6330`).
3. Mapped live endpoints: overview metrics, named chart endpoints, options endpoints.
4. Enumerated available charts: revenue, mrr, churn, subscription_retention, trial_conversion_rate, actives, customers_active, trials, conversion_to_paying, customers_new, and others.
5. Confirmed filters, segments, and resolution options are rich and usable.
6. Noted rate limit of 15 rpm on chart domain.

### Community research
7. Reviewed RevenueCat community threads about Charts API demand.
8. Found multi-year pattern of users requesting API access to chart/export data and customizable operator dashboards.
9. Reviewed adjacent tools and competitor analytics approaches.

### Concept selection
10. Generated 6 candidate tool concepts.
11. Ran two structured review rounds:
    - Round 1: technical architecture + growth/founder usefulness
    - Round 2: technical feasibility, audience fit, hiring-judge lens, red-team critique
12. Each review round used evidence-grounded prompts with the real API findings.
13. Consensus emerged: build the Weekly Growth Brief / Monetization Operator as the core product, with a thin command-center shell.
14. Key principle locked: build the insight layer, not a dashboard clone.

### Key tradeoffs decided
- Deterministic rules over speculative AI analysis
- Thin shell over full dashboard rebuild
- Conservative claims over fake confidence
- Rate metrics averaged, not summed
- Mock preview mode for reviewer safety

## Phase 2 — Build (hours 2–4)

### Implementation
15. Scaffolded Next.js + TypeScript app.
16. Integrated RevenueCat API v2 layer with env-based secret key.
17. Built deterministic brief generation engine in `src/lib/brief.ts`.
18. Created mock data layer for review-safe fallback.
19. Built brief-first homepage: investigation queue primary, KPI strip secondary, supporting charts tertiary.
20. Added `/api/brief` JSON endpoint for agent/export consumption.

### Review-driven corrections
21. Ran expert review team (architecture, devrel, growth, evaluator) against the first build.
22. Fixed rate-metric math: rates now use windowed averages, not summed percentages.
23. Removed fake metric aliasing that mapped unrelated charts together.
24. Added cross-metric contradiction detection (e.g. trials up + conversion down).
25. Corrected README setup path and added proof findings.
26. Rewrote social pack around a proof-driven launch wedge.

## Phase 3 — Content package (hours 4–6)

### Launch post
27. Drafted 1,500+ word technical blog post (`BLOG_POST.md`).
28. Added real API walkthrough with endpoint examples.
29. Added "What this taught me about the Charts API" section.
30. Added sample operator brief from live Dark Noise data.
31. Added explicit limitations section.

### Video
32. Wrote video script (`VIDEO_SCRIPT.md`) for 1–3 minute demo.

### Social
33. Created 5 social posts (`SOCIAL_POSTS.md`) around proof-driven launch wedge.

## Phase 4 — Growth campaign (hours 4–6)

34. Designed growth campaign (`GROWTH_CAMPAIGN.md`) with:
    - audience tiers ranked by fit
    - day-by-day campaign sequence
    - at least 3 target communities with specific accounts and disclosure
    - $100 budget allocation
    - measurement plan

## Phase 5 — Assembly & polish (ongoing)

35. Created submission index (`SUBMISSION_INDEX.md`).
36. Created architecture doc (`ARCHITECTURE.md`).
37. Captured live sample chart output (`live-sample-output.json`).
38. Created sample findings from real data (`SAMPLE_FINDINGS.md`).

## Tools used
- RevenueCat API v2
- Next.js 16 + TypeScript + Tailwind CSS
- OpenClaw agent infrastructure (Kit)
- Structured sub-agent review passes for quality assurance
- GitHub (KitTheRevenueCat account)
- Web search and fetch for research

## Key decisions log
| Decision | Reasoning |
|----------|-----------|
| Brief-first, not dashboard clone | Dashboard clones are commodity; the insight layer is the real gap |
| Deterministic rules, not LLM analysis | Trustworthiness matters more than impressiveness for this prototype |
| Averaged rates, not summed | Summing percentage metrics is analytically sloppy |
| Mock preview mode | Makes the app safely reviewable without secrets |
| One launch wedge | "AI agent for weekly subscription ops" is more novel than generic operator tooling |
| Conservative limitations section | Honest constraint framing builds evaluator trust |
