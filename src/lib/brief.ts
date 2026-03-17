import type { ChartResponse, OverviewMetric } from "./revenuecat";

export type BriefSection = {
  title: string;
  summary: string;
  evidence: string;
  action: string;
};

export type GrowthBrief = {
  headline: string;
  kpis: { label: string; value: string }[];
  sections: BriefSection[];
};

function formatNumber(value: number, unit: string) {
  if (unit === "$") return `$${Math.round(value).toLocaleString()}`;
  if (unit === "%") return `${value.toFixed(1)}%`;
  return Math.round(value).toLocaleString();
}

function chartSeries(chart: ChartResponse, measureName?: string) {
  const measureIndex = measureName
    ? chart.measures.findIndex((m) => m.display_name === measureName)
    : 0;
  const index = measureIndex >= 0 ? measureIndex : 0;

  return chart.values
    .filter((v) => v.measure === index && !v.incomplete)
    .sort((a, b) => a.cohort - b.cohort);
}

function compareRecent(chart: ChartResponse, measureName?: string, size = 7) {
  const series = chartSeries(chart, measureName);
  const recent = series.slice(-size);
  const prior = series.slice(-(size * 2), -size);

  const recentSum = recent.reduce((sum, point) => sum + point.value, 0);
  const priorSum = prior.reduce((sum, point) => sum + point.value, 0);
  const delta = priorSum === 0 ? 0 : ((recentSum - priorSum) / priorSum) * 100;

  return {
    recentSum,
    priorSum,
    delta,
    points: series,
  };
}

export function generateGrowthBrief(input: {
  overview: OverviewMetric[];
  charts: Record<string, ChartResponse>;
}): GrowthBrief {
  const metric = (id: string) => input.overview.find((m) => m.id === id);

  const revenue = compareRecent(input.charts.revenue, "Revenue");
  const trials = compareRecent(input.charts.trials);
  const customers = compareRecent(input.charts.customers_new);
  const conversion = compareRecent(input.charts.trial_conversion_rate, "Conversion Rate");
  const churn = compareRecent(input.charts.churn);

  const sections: BriefSection[] = [];

  if (revenue.delta > 5) {
    sections.push({
      title: "Revenue momentum improved",
      summary: `Revenue increased ${revenue.delta.toFixed(1)}% versus the prior comparison window.`,
      evidence: `Recent period revenue ${formatNumber(revenue.recentSum, "$" )} vs prior ${formatNumber(revenue.priorSum, "$")}.`,
      action: "Check which product duration, offering, or acquisition segment contributed most and consider doubling down on that mix in the next promotion or paywall test.",
    });
  } else if (revenue.delta < -5) {
    sections.push({
      title: "Revenue slowed materially",
      summary: `Revenue declined ${Math.abs(revenue.delta).toFixed(1)}% versus the prior comparison window.`,
      evidence: `Recent period revenue ${formatNumber(revenue.recentSum, "$" )} vs prior ${formatNumber(revenue.priorSum, "$")}.`,
      action: "Review whether trial starts, conversion rate, or churn moved against you. Start with paywall traffic quality and renewal/cancellation patterns before changing pricing.",
    });
  }

  if (conversion.delta < -5) {
    sections.push({
      title: "Trial conversion weakened",
      summary: `Trial conversion rate fell ${Math.abs(conversion.delta).toFixed(1)}% compared with the prior period.`,
      evidence: `Recent conversion signal ${conversion.recentSum.toFixed(1)} vs prior ${conversion.priorSum.toFixed(1)} on aggregated chart values.`,
      action: "Inspect paywall message-to-offer fit, introductory offer mix, and whether a traffic/channel shift is bringing in lower-intent users.",
    });
  } else if (conversion.delta > 5) {
    sections.push({
      title: "Trial conversion improved",
      summary: `Trial conversion rate improved ${conversion.delta.toFixed(1)}% versus the prior period.`,
      evidence: `Recent conversion signal ${conversion.recentSum.toFixed(1)} vs prior ${conversion.priorSum.toFixed(1)} on aggregated chart values.`,
      action: "Capture what changed recently — paywall copy, acquisition mix, product mix, or offer structure — so you can intentionally preserve the lift.",
    });
  }

  if (churn.delta > 5) {
    sections.push({
      title: "Churn pressure increased",
      summary: `Churn moved up ${churn.delta.toFixed(1)}% versus the prior period.`,
      evidence: `Recent churn signal ${churn.recentSum.toFixed(1)} vs prior ${churn.priorSum.toFixed(1)}.`,
      action: "Review cancellation timing, renewal-cycle cohorts, and whether a recent acquisition push brought in lower-retention subscribers.",
    });
  }

  if (trials.delta > 5 && conversion.delta <= 0) {
    sections.push({
      title: "Top-of-funnel grew faster than conversion",
      summary: `Trial starts increased ${trials.delta.toFixed(1)}%, but conversion did not improve alongside them.`,
      evidence: `Trials recent ${formatNumber(trials.recentSum, "#")} vs prior ${formatNumber(trials.priorSum, "#")}.`,
      action: "Treat this as a traffic-quality or paywall-fit investigation. More trials are only good if conversion and retention stay healthy.",
    });
  }

  const contradictions: BriefSection[] = [];

  if (trials.delta > 5 && conversion.delta < -5) {
    contradictions.push({
      title: "Acquisition quality check",
      summary: "Trial volume increased, but conversion quality fell. Top-of-funnel growth is outpacing monetization efficiency.",
      evidence: `Trials ${trials.delta.toFixed(1)}% vs prior period while conversion rate moved ${conversion.delta.toFixed(1)}%.`,
      action: "Investigate paywall fit first: review offer mix, price anchoring, and whether channel mix shifted toward lower-intent traffic.",
    });
  }

  if (customers.delta > 5 && revenue.delta <= 0) {
    contradictions.push({
      title: "Revenue quality check",
      summary: "Customer growth improved without a matching revenue lift.",
      evidence: `New customers moved ${customers.delta.toFixed(1)}% while revenue moved ${revenue.delta.toFixed(1)}%.`,
      action: "Check product mix and whether lower-priced or trial-heavy acquisition is diluting short-term monetization quality.",
    });
  }

  sections.unshift(...contradictions);

  if (sections.length === 0) {
    sections.push({
      title: "Subscription performance is relatively stable",
      summary: "No major swing crossed the current operator-alert thresholds across the core tracked charts.",
      evidence: "Revenue, trials, conversion, churn, and customer growth all stayed within a narrow comparison band.",
      action: "Use segmentation next: compare by product duration, platform, store, or acquisition source to find hidden pockets of weakness or strength.",
    });
  }

  return {
    headline: "Weekly Monetization Operator Brief",
    kpis: [
      metric("mrr"),
      metric("revenue"),
      metric("new_customers"),
      metric("active_subscriptions"),
      metric("active_trials"),
    ]
      .filter(Boolean)
      .map((m) => ({ label: m!.name, value: formatNumber(m!.value, m!.unit) })),
    sections,
  };
}
