const API_BASE = "https://api.revenuecat.com/v2";

export type OverviewMetric = {
  id: string;
  name: string;
  description: string;
  period: string;
  unit: string;
  value: number;
  last_updated_at_iso8601?: string | null;
};

export type OverviewResponse = {
  metrics: OverviewMetric[];
  object: string;
};

export type ChartValue = {
  cohort: number;
  incomplete: boolean;
  measure: number;
  value: number;
};

export type ChartMeasure = {
  chartable: boolean;
  decimal_precision: number;
  description: string;
  display_name: string;
  tabulable: boolean;
  unit: string;
};

export type ChartResponse = {
  category: string;
  description: string;
  display_name: string;
  display_type: string;
  documentation_link?: string;
  start_date: number;
  end_date: number;
  resolution: string;
  measures: ChartMeasure[];
  summary?: Record<string, Record<string, number>>;
  values: ChartValue[];
  user_selectors?: Record<string, string>;
};

function getKey() {
  const key = process.env.REVENUECAT_API_KEY;
  if (!key) {
    throw new Error("Missing REVENUECAT_API_KEY env var");
  }
  return key;
}

async function rcFetch<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      Authorization: `Bearer ${getKey()}`,
    },
    next: { revalidate: 3600 },
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`RevenueCat API error ${res.status}: ${text}`);
  }

  return res.json() as Promise<T>;
}

export async function getProjects() {
  return rcFetch<{ items: { id: string; name: string }[] }>("/projects");
}

export async function getOverview(projectId: string) {
  return rcFetch<OverviewResponse>(`/projects/${projectId}/metrics/overview`);
}

export async function getChart(projectId: string, chartName: string) {
  return rcFetch<ChartResponse>(`/projects/${projectId}/charts/${chartName}?realtime=true`);
}

export function hasRevenueCatKey() {
  return Boolean(process.env.REVENUECAT_API_KEY);
}
