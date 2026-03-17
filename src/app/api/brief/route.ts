import { NextResponse } from "next/server";
import { generateGrowthBrief } from "@/lib/brief";
import { mockCharts, mockOverview } from "@/lib/mock-data";
import { getChart, getOverview, hasRevenueCatKey } from "@/lib/revenuecat";

const PROJECT_ID = process.env.REVENUECAT_PROJECT_ID || "proj058a6330";
const CHARTS = ["revenue", "mrr", "trial_conversion_rate", "churn", "customers_new", "trials"] as const;

export async function GET() {
  const useMock = !hasRevenueCatKey();

  const overview = useMock ? mockOverview : await getOverview(PROJECT_ID);
  const chartResponses = useMock
    ? CHARTS.map((name) => mockCharts[name])
    : await Promise.all(CHARTS.map((chart) => getChart(PROJECT_ID, chart)));

  const chartMap = Object.fromEntries(CHARTS.map((name, i) => [name, chartResponses[i]]));
  const brief = generateGrowthBrief({
    overview: overview.metrics,
    charts: {
      revenue: chartMap.revenue,
      mrr: chartMap.mrr,
      trial_conversion_rate: chartMap.trial_conversion_rate,
      churn: chartMap.churn,
      customers_new: chartMap.customers_new,
      trials: chartMap.trials,
    },
  });

  return NextResponse.json({
    generated_at: new Date().toISOString(),
    mode: useMock ? "mock" : "live",
    brief,
  });
}
