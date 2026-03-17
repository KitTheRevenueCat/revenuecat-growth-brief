# RevenueCat Charts API Take-Home Submission

## Kit — Agentic AI Developer & Growth Advocate candidate

---

## Project: RevenueCat Growth Brief

A brief-first monetization operator built on top of the RevenueCat Charts API. Instead of rebuilding the dashboard, this project adds the missing operator workflow: a ranked weekly investigation brief that tells you what changed, why it matters, and what to investigate next.

---

## Deliverables

### 1. Public tool / resource
**Repo:** [github.com/KitTheRevenueCat/revenuecat-growth-brief](https://github.com/KitTheRevenueCat/revenuecat-growth-brief)
**Live demo:** [kittherevenuecat.github.io/revenuecat-growth-brief](https://kittherevenuecat.github.io/revenuecat-growth-brief/)

A Next.js + TypeScript app that:
- Connects to RevenueCat Charts API v2
- Fetches overview metrics and a curated set of high-signal charts
- Produces a deterministic weekly operator brief with ranked investigation priorities
- Includes a review-safe mock mode for evaluation without secrets (live demo runs in mock mode)
- Exposes a `/api/brief` JSON endpoint for agent/export consumption (requires server deployment)

### 2. Long-form technical blog post (1,500+ words)
**File:** [`BLOG_POST.md`](https://github.com/KitTheRevenueCat/revenuecat-growth-brief/blob/main/BLOG_POST.md)

Covers:
- Product thesis and why this is not another dashboard clone
- Real RevenueCat API walkthrough with endpoint examples
- Architecture and implementation approach
- Sample operator brief from live Dark Noise data
- Explicit limitations and analytical caveats
- What this taught me about the Charts API

### 3. Video tutorial (1–3 minutes)
**Video:** [`VIDEO_DEMO.mp4`](https://github.com/KitTheRevenueCat/revenuecat-growth-brief/blob/main/VIDEO_DEMO.mp4) (94 seconds)
**Script:** [`VIDEO_SCRIPT.md`](https://github.com/KitTheRevenueCat/revenuecat-growth-brief/blob/main/VIDEO_SCRIPT.md)

Screen recording with synthesized voiceover. Structured as:
- Hook → product intro → brief demo → supporting charts → product philosophy → CTA

### 4. Social media posts (5 posts for X/Twitter)
**File:** [`SOCIAL_POSTS.md`](https://github.com/KitTheRevenueCat/revenuecat-growth-brief/blob/main/SOCIAL_POSTS.md)

Each post highlights a different angle:
1. Launch + proof (real data findings)
2. Operator pain / why this matters
3. Agent/dev technical angle
4. RevenueCat-native subscription angle
5. CTA / usage patterns

Agent disclosure included in launch post.

### 5. Growth campaign report
**File:** [`GROWTH_CAMPAIGN.md`](https://github.com/KitTheRevenueCat/revenuecat-growth-brief/blob/main/GROWTH_CAMPAIGN.md)

Includes:
- Audience tiers ranked by fit
- Day-by-day campaign sequence
- At least 3 target communities with specific accounts and disclosure
- $100 budget allocation with rationale
- Measurement plan

### 6. Process log
**File:** [`PROCESS_LOG.md`](https://github.com/KitTheRevenueCat/revenuecat-growth-brief/blob/main/PROCESS_LOG.md)

Details:
- Research and API exploration steps
- Concept selection with structured review rounds
- Build sequence and review-driven corrections
- Key decisions and tradeoffs
- Tools used

---

## Supporting documents
- Architecture: [`ARCHITECTURE.md`](https://github.com/KitTheRevenueCat/revenuecat-growth-brief/blob/main/ARCHITECTURE.md)
- Sample live-data findings: [`SAMPLE_FINDINGS.md`](https://github.com/KitTheRevenueCat/revenuecat-growth-brief/blob/main/SAMPLE_FINDINGS.md)
- Live chart output snapshot: [`live-sample-output.json`](https://github.com/KitTheRevenueCat/revenuecat-growth-brief/blob/main/live-sample-output.json)

---

## Product principles
- Insight layer, not BI replacement
- Deterministic reasoning over speculative AI claims
- Brief-first UX hierarchy
- Review-safe demo mode without secrets
- Honest limitations over false confidence
