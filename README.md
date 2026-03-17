# RevenueCat Growth Brief

A brief-first monetization operator built on top of the RevenueCat Charts API.

**[Live Demo →](https://kittherevenuecat.github.io/revenuecat-growth-brief/)** (mock review-safe mode) | **[Video Walkthrough →](https://github.com/KitTheRevenueCat/revenuecat-growth-brief/blob/main/VIDEO_DEMO.mp4)** (94s)

## What it is

RevenueCat Growth Brief is a lightweight operator tool for subscription apps. It combines a thin command-center shell with a rules-based weekly brief that answers three practical questions:

1. What changed?
2. Why does it matter?
3. What should I investigate next?

Instead of trying to rebuild RevenueCat's dashboard, this project focuses on the insight layer: a compact set of KPIs and charts, plus a generated weekly monetization brief that teams can use in an operating cadence.

## Why this exists

RevenueCat's Charts API already exposes the hard part: subscription-native metrics such as revenue, MRR, churn, trials, conversion, retention, and customer growth.

What many operators still need is a faster way to turn those charts into decisions.

This project is the answer to that gap.

## Product direction

- **Core product:** Weekly Growth Brief / Monetization Operator
- **UI shape:** Thin command-center shell
- **Non-goals:** Full BI replacement, forecasting, experiment attribution, fake AI root-cause claims

## Current scope

This first pass ships with:

- Brief-first homepage hierarchy
- Overview KPI cards
- Curated supporting charts:
  - Revenue
  - MRR
  - Trial Conversion Rate
  - Churn
- A deterministic weekly brief generated from recent chart deltas and cross-metric contradictions
- Real RevenueCat API integration using a secret key from environment variables
- Mock review-safe mode when no secret key is present

## Setup

```bash
npm install
npm run dev
```

For live RevenueCat data:

```bash
REVENUECAT_API_KEY=your_v2_secret_key npm run dev
```

Optional:

```bash
REVENUECAT_PROJECT_ID=proj058a6330
```

If `REVENUECAT_PROJECT_ID` is omitted, the app defaults to the Dark Noise project used for the take-home assignment.

## Environment variables

- `REVENUECAT_API_KEY` — required, RevenueCat API v2 secret key
- `REVENUECAT_PROJECT_ID` — optional, RevenueCat project id

## Technical notes

The app uses:

- Next.js App Router
- TypeScript
- server-side fetches against RevenueCat API v2
- deterministic rules in `src/lib/brief.ts`

The brief generator intentionally stays conservative:

- compares recent windows
- identifies significant movement
- maps metric deltas to operator guidance
- avoids causality and prediction claims the API does not support directly

## What to build next

- export/share weekly brief as Markdown / email / Slack payload
- add one controlled segmentation workflow
- add chart drill-down links
- support a small library of operator templates (growth, retention, pricing mix)


## Why this is not just another dashboard

RevenueCat already has charts. The problem this project addresses is the operator workflow around those charts:

- what changed this week?
- what deserves attention first?
- what should I investigate next?

This is why the product is brief-first. The dashboard shell exists to support the weekly operating brief, not the other way around.

## Current operator workflow

1. Load overview metrics and a curated set of high-signal charts
2. Compare the latest 7 data points against the prior 7
3. Detect notable movement and cross-metric contradictions
4. Produce a ranked investigation queue
5. Support that queue with evidence charts

## Intentional tradeoffs

What this prototype intentionally does **not** do:

- claim causal inference
- forecast outcomes
- run experiment analysis
- rebuild every RevenueCat chart
- pretend weak signals are strong signals

That constraint discipline is part of the product thesis.


## Sample live-data findings

Using the provided Dark Noise project data, the current prototype surfaced signals such as:

- Revenue up roughly **14.7%** versus the prior comparison window
- Trial volume up roughly **14.7%**
- New customers up roughly **1.2%**
- MRR slightly down roughly **3.0%**

That combination is exactly the kind of operator pattern this project is meant to highlight: top-of-funnel and short-term revenue can improve while recurring revenue quality tells a more mixed story.

See `SAMPLE_FINDINGS.md` and `live-sample-output.json` for the captured proof artifacts.
