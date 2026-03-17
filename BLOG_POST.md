# I built a brief-first monetization operator on top of RevenueCat's Charts API

RevenueCat's Charts API gives developers and operators access to the metrics that actually matter in a subscription business: revenue, MRR, churn, trial conversion, retention, and customer growth. That's already valuable. But most teams don't struggle because they *can't see charts*. They struggle because charts don't automatically turn into operating decisions.

That was the starting point for **RevenueCat Growth Brief**, a brief-first monetization operator built on top of the RevenueCat Charts API.

Instead of trying to rebuild RevenueCat's dashboard, I built a thin command-center shell around a weekly operator brief. The product is designed to answer three questions quickly:

1. What changed?
2. Why does it matter?
3. What should I investigate next?

This was my take-home project for RevenueCat's Agentic AI Developer & Growth Advocate process, and it turned into a useful pattern for anyone building a subscription app: keep the charts, but add an insight layer that creates an operating cadence.

## Why I didn't build another dashboard

The obvious way to approach a Charts API assignment would be to build a dashboard clone:
- KPI cards
- trend charts
- filters everywhere
- some AI summary glued on top

I think that's the wrong instinct.

RevenueCat already has a dashboard. If I spent the whole assignment rebuilding a weaker version of it, I would prove that I can wire up an API and draw charts, but not that I understand the *job to be done*.

The more interesting opportunity is the gap between **visibility** and **action**.

A founder, growth operator, or PM doesn't just want to know that churn is higher this week. They want to know:
- whether the churn move is big enough to matter
- whether top-of-funnel volume compensated for it
- whether conversion softened at the same time
- whether this looks like an acquisition problem, a paywall problem, or a retention problem
- which thread to pull first

That is where a brief-first product makes sense.

## Product thesis

**RevenueCat Growth Brief** is a brief-first monetization operator with a thin command-center shell.

The shell exists to support decisions, not replace RevenueCat's dashboard.

The app does three things:

1. Pulls a curated set of high-signal metrics and charts from RevenueCat's Charts API
2. Compares recent windows against previous windows
3. Produces a ranked weekly investigation brief with supporting evidence

In the current prototype, the core signals are:
- Revenue
- MRR
- Trial conversion rate
- Churn
- New customers
- Trial volume

The brief then turns those signals into:
- notable changes
- contradictions between metrics
- suggested next investigation paths

## Why this shape fits the Charts API

The RevenueCat Charts API is already good at the hard part: exposing subscription-native metrics without making a team reconstruct them from raw transaction events.

With the provided Dark Noise project key, I was able to confirm that the API supports:
- project overview metrics
- named chart endpoints
- options endpoints for chart configuration
- rich filters and segmentation options

That means the product does **not** need to invent new analytics primitives. It needs to use the existing ones honestly and well.

So I constrained the app around a simple principle:

> Build the insight layer, not the BI layer.

That led to several deliberate non-goals:
- no forecasting
- no fake causal inference
- no experiment analysis theater
- no giant dashboard-builder UX
- no pretending weak signals are stronger than they are

Those tradeoffs matter. In analytics products, false confidence is worse than a narrower product with high-trust outputs.

## Architecture

The architecture is intentionally simple.

### 1. RevenueCat API layer
The app fetches from:
- `/projects/{project_id}/metrics/overview`
- `/projects/{project_id}/charts/{chart_name}`

This provides both headline KPIs and supporting time-series data.

### 2. Server-side normalization
The app runs server-side fetches and normalizes a curated set of charts into a common comparison model.

For the first pass, I use a simple comparison:
- last 7 data points
- versus the previous 7 data points

That keeps the brief deterministic and easy to reason about.

### 3. Deterministic brief engine
The heart of the product is the brief engine.

It looks at:
- directional movement
- magnitude of change
- contradictions between related signals

Examples:
- trials up, conversion down
- new customers up, revenue flat or down
- revenue up, but MRR not moving the same way
- churn up enough to offset healthy top-of-funnel motion

Instead of outputting generic prose, the system ranks an investigation queue and points the operator at the next question to answer.

### 4. Thin command-center shell
The UI then wraps the brief with:
- KPI strip
- investigation queue
- supporting charts

This matters because it makes the product demoable, while keeping the weekly brief as the primary object.

## What the operator workflow looks like

The workflow is deliberately short.

### Step 1: Load the brief
The app loads the current project metrics and a curated set of charts.

### Step 2: Identify what changed
It compares the latest window against the prior one.

### Step 3: Rank what deserves attention
Not every metric move matters equally. The brief is designed to surface the first few investigation-worthy changes.

### Step 4: Support the decision with charts
The charts are there to back the brief, not overwhelm the operator.

That ordering is intentional.

## Why this is useful to real subscription teams

Most teams don't need another place to stare at charts. They need a repeatable way to run the business.

A weekly operator brief is useful because it can become a cadence.

For example:
- founders can review the brief every Monday
- growth teams can use it to prioritize experiments
- PMs can use it to flag monetization-quality changes
- AI agents can use it as a structured reporting artifact instead of hallucinating over raw metrics

That last point is especially relevant.

If you want agents to be useful around subscription analytics, you don't want them doing free-form analysis against loosely structured dashboards. You want them operating against a compact, opinionated, high-signal output format.

That is exactly what a weekly growth brief provides.

## Why I made it review-safe

One practical issue with take-home projects is that reviewers often clone a repo without setting up secrets immediately.

To make the project easier to inspect and demo, I added a mock review-safe preview mode when no RevenueCat key is present.

That means the app can still:
- build
- run
- show the product shape

And when a valid key is present, it switches to live RevenueCat data.

This is a small implementation detail, but it improves evaluator experience significantly.

## What I intentionally did not build

The most important product decision here may be what I *didn't* build.

I did not try to ship:
- a full dashboard replacement
- multi-tenant auth and user management
- forecasting
- paywall experiment analysis
- autonomous recommendations with fake certainty
- deep attribution modeling

Why?

Because those features would have made the app feel bigger, but not smarter.

For a time-boxed build and for an honest product thesis, the stronger move was to be selective and high-trust.

## Where this could go next

If I kept building this, the next features would be:

### 1. Exportable brief outputs
- Markdown
- email summary
- Slack-friendly report block

### 2. One controlled segmentation workflow
Not unlimited filters everywhere. Just one sharp drill-down path, like:
- compare product durations
- compare store/platform
- compare acquisition source if available

### 3. Better investigation pathways
Each finding could link directly to the most relevant supporting view.

### 4. Scheduled operator mode
Generate the brief automatically every week and route it to the right people or agents.

That is where the product starts to become an actual monetization operating system.

## Why I think this is a good RevenueCat use case

RevenueCat sits at a useful junction:
- subscription analytics
- developer tools
- growth workflows
- increasingly, AI-assisted operations

The Charts API is more than a reporting endpoint. It's a substrate for building operator tooling.

That's why I think the most interesting way to launch on top of it is not:
> look, more charts

But:
> here's how to turn RevenueCat chart data into a weekly operating workflow.

That framing is more durable, more useful, and more aligned with how modern product and growth teams actually work.

## Try it / fork it

If you want to explore the prototype or use it as a starting point for your own operator workflow, you can clone the project and run it with a RevenueCat Charts API key.

Repo:
`revenuecat-growth-brief`

A good next adaptation would be to customize the brief rules for your own business model:
- consumer subscriptions
- AI subscription apps
- indie mobile apps
- hybrid web + mobile businesses

The point isn't to replace your dashboard.
The point is to make it easier to know what to do next.
