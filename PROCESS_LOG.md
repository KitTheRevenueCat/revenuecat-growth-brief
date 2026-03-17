# RevenueCat Growth Brief — Process Log

## Objective
Create a useful public tool/resource built on top of RevenueCat's Charts API, then package it with launch content and a growth campaign.

## Key decisions
- Rejected a generic dashboard clone in favor of a brief-first operator product.
- Chose deterministic insights over speculative AI analysis.
- Chose a thin command-center shell to support the brief, not replace the dashboard.
- Added mock preview mode so the artifact remains review-safe without secrets.

## Research steps
1. Read the take-home assignment in full.
2. Verified the provided API key against RevenueCat API v2.
3. Confirmed Dark Noise project access.
4. Mapped live endpoints for overview metrics and charts.
5. Enumerated chart capabilities, filters, segments, and rate-limit implications.
6. Reviewed RevenueCat community demand around chart/export API access and operator dashboards.
7. Ran structured review passes across technical, audience, hiring, and red-team lenses.

## Tradeoffs
- Did not build forecasting, experiment attribution, or fake causal analysis.
- Did not rebuild the full RevenueCat dashboard.
- Chose a smaller, more trustworthy artifact over a broader but weaker one.

## Build sequence
1. Scaffolded Next.js + TypeScript app
2. Integrated RevenueCat API layer
3. Added rules-based brief generation
4. Tightened brief-first product shape
5. Added fallback/mock mode for reviewability
6. Wrote launch post, video script, social pack, and growth campaign draft

## Remaining work
- polish app/demo visuals
- capture screenshots/video
- tighten launch materials into final submission format
