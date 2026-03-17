# RevenueCat Growth Brief — Architecture

## Product thesis
RevenueCat already gives operators access to subscription-native metrics through Charts. This project adds the missing layer: a brief-first operator workflow that turns chart data into a ranked weekly investigation queue.

## System flow
1. RevenueCat API v2
   - `/projects/{project_id}/metrics/overview`
   - `/projects/{project_id}/charts/{chart_name}`
2. Server-side normalization layer
   - fetch curated metrics and chart series
   - normalize recent comparison windows
3. Deterministic brief engine
   - detect notable metric movements
   - detect cross-metric contradictions
   - rank investigation priorities
4. Thin command-center shell
   - KPI strip
   - investigation queue
   - supporting charts
   - weekly operator brief

## Non-goals
- BI replacement
- forecasting
- experiment attribution
- causal inference
- full dashboard builder

## Why this shape
The take-home is time-bounded. A brief-first product lets us prove product judgment, technical execution, and growth narrative without wasting time cloning RevenueCat's dashboard.
