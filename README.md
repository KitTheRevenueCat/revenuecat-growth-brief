# RevenueCat Growth Brief

**A subscription contradiction detector built on RevenueCat's Charts API.**

Revenue up 14.7%. MRR down 3.0%. Your dashboard shows green. Your business tells a different story.

**[Live Demo →](https://kittherevenuecat.github.io/revenuecat-growth-brief/)** | **[Blog Post →](https://kittherevenuecat.github.io/revenuecat-growth-brief/blog.html)** | **[Video →](https://kittherevenuecat.github.io/revenuecat-growth-brief/video.html)** (under 2 min)

## What it does

RevenueCat Growth Brief applies a deterministic rule set across a curated set of RevenueCat charts to surface operator-relevant metric contradictions.

Every week, it answers three questions:

1. **What changed?** — which metrics moved enough to matter
2. **What contradicts?** — revenue up but MRR down? trials up but conversion down?
3. **What do you investigate first?** — a ranked queue, not a wall of charts

Instead of rebuilding RevenueCat's dashboard, this project adds the missing layer: a contradiction detector that turns chart data into an operating cadence.

## Why this exists

RevenueCat's Charts API already exposes the hard part: subscription-native metrics such as revenue, MRR, churn, trials, conversion, retention, and customer growth.

What many operators still need is a faster way to turn those charts into decisions.

This project is one prototype response to that gap. It currently analyzes a curated subset of charts using fixed heuristic thresholds and does not yet support segmentation, experiment context, or customizable alert logic.

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
4. Produce an ordered investigation queue based on fixed rule priority
5. Support that queue with evidence charts

## Intentional tradeoffs

What this prototype intentionally does **not** do:

- claim causal inference
- forecast outcomes
- run experiment analysis
- rebuild every RevenueCat chart
- pretend weak signals are strong signals

That constraint discipline is part of the product thesis.


## What this does NOT demonstrate yet

This prototype exercises RevenueCat's Charts API v2, but it does not yet demonstrate:

- **App-side SDK integration** — configuring `Purchases.configure()`, handling `CustomerInfo` updates, managing subscription lifecycle events in Swift/Kotlin/Flutter/RN
- **Entitlements and offerings setup** — creating offerings in the RC dashboard, mapping products to entitlements, A/B testing paywall configurations
- **Paywall presentation** — RevenueCat Paywalls SDK, `PaywallView` in SwiftUI, template customization, paywall events
- **Webhook handling** — processing `INITIAL_PURCHASE`, `RENEWAL`, `CANCELLATION`, `BILLING_ISSUE` events server-side for downstream automation
- **Experiment instrumentation** — setting up pricing experiments, measuring trial-to-paid conversion by cohort, interpreting experiment results

These would be the next artifacts for a fuller developer-advocate portfolio. The existing [StoreKit 2 + RevenueCat reference implementation](https://github.com/KitTheRevenueCat/storekit2-revenuecat) demonstrates some of these patterns (purchase flow, entitlement checking, SwiftUI paywall, restore purchases).

## Sample live-data findings

Using the provided Dark Noise project data, the current prototype surfaced signals such as:

- Revenue up roughly **14.7%** versus the prior comparison window
- Trial volume up roughly **14.7%**
- New customers up roughly **1.2%**
- MRR slightly down roughly **3.0%**

That combination is exactly the kind of operator pattern this project is meant to highlight: top-of-funnel and short-term revenue can improve while recurring revenue quality tells a more mixed story.

See `SAMPLE_FINDINGS.md` and `live-sample-output.json` for the captured proof artifacts.
