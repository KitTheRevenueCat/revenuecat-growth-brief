# Sample live-data findings

> Captured from the Dark Noise project via RevenueCat Charts API v2.
> Note: the live API returns churn as absolute subscriber counts, not percentages.
> The mock/demo mode uses synthetic percentage-based churn for illustration purposes.

## Revenue (unit: $)
- **recent (7-day sum):** $1,452.76
- **prior (7-day sum):** $1,266.73
- **delta:** +14.7%

## MRR (unit: $)
- **recent (7-day sum):** $31,310.14
- **prior (7-day sum):** $32,271.56
- **delta:** -3.0%

## Trial conversion rate (unit: %)
- **recent (7-day avg):** 0.00%
- **prior (7-day avg):** 0.00%
- **delta:** 0.0%
- **Note:** Dark Noise appears to have no active trial-to-paid conversion activity in this window. This is expected for an established indie app with stable subscriber base. The mock demo uses synthetic conversion data to demonstrate the brief's contradiction-detection capability.

## Churn (unit: # — subscriber count, not percentage)
- **recent (7-day sum):** 17,655
- **prior (7-day sum):** 17,629
- **delta:** +0.1%
- **Note:** The Charts API returns churn as raw subscriber counts for this project, not as a churn rate percentage. The brief engine handles this correctly by checking the `unit` field from the chart's `measures` array. When unit is `#`, values are summed; when unit is `%`, values are averaged.

## New customers (unit: #)
- **recent (7-day sum):** 426
- **prior (7-day sum):** 421
- **delta:** +1.2%

## Trials (unit: #)
- **recent (7-day sum):** 436
- **prior (7-day sum):** 380
- **delta:** +14.7%

---

## Key observation

The most interesting signal from the live data: revenue grew 14.7% and trials grew 14.7%, but MRR declined 3.0%. This suggests the revenue lift may have come from non-recurring sources (annual renewals, lifetime purchases) rather than new monthly subscriptions. That is exactly the kind of contradiction this operator brief is designed to surface.

## Mock vs. live data

The live demo at kittherevenuecat.github.io/revenuecat-growth-brief runs in mock mode (no API key). The mock data uses synthetic values that demonstrate more diverse brief findings, including churn-as-percentage and non-zero conversion rates. This is documented in the README. The live-API behavior is demonstrated through this sample findings document and the captured `live-sample-output.json`.
