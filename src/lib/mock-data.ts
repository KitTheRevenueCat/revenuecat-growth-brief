import type { ChartResponse, OverviewResponse } from "./revenuecat";

const now = 1773705600;
const days = Array.from({ length: 14 }, (_, i) => now - (13 - i) * 86400);

function makeChart(name: string, description: string, unit: string, values: number[]): ChartResponse {
  return {
    category: "mock",
    description,
    display_name: name,
    display_type: "default",
    start_date: days[0],
    end_date: days[days.length - 1],
    resolution: "day",
    measures: [
      {
        chartable: true,
        decimal_precision: unit === "%" ? 1 : 0,
        description: name,
        display_name: name,
        tabulable: true,
        unit,
      },
    ],
    summary: {
      total: {
        [name]: values.reduce((a, b) => a + b, 0),
      },
    },
    values: values.map((value, index) => ({
      cohort: days[index],
      incomplete: false,
      measure: 0,
      value,
    })),
    user_selectors: {},
  };
}

export const mockOverview: OverviewResponse = {
  object: "overview_metrics",
  metrics: [
    { id: "mrr", name: "MRR", description: "Monthly Recurring Revenue", period: "P28D", unit: "$", value: 4554 },
    { id: "revenue", name: "Revenue", description: "Last 28 days", period: "P28D", unit: "$", value: 5126 },
    { id: "new_customers", name: "New Customers", description: "Last 28 days", period: "P28D", unit: "#", value: 1570 },
    { id: "active_subscriptions", name: "Active Subscriptions", description: "In total", period: "P0D", unit: "#", value: 2528 },
    { id: "active_trials", name: "Active Trials", description: "In total", period: "P0D", unit: "#", value: 65 },
  ],
};

export const mockCharts = {
  revenue: makeChart("Revenue", "Revenue generated over time.", "$", [120, 150, 160, 140, 180, 210, 190, 170, 165, 155, 145, 160, 175, 200]),
  mrr: makeChart("MRR", "Monthly recurring revenue trend.", "$", [3900, 3920, 3950, 3980, 4010, 4060, 4090, 4120, 4180, 4250, 4310, 4380, 4450, 4554]),
  trial_conversion_rate: makeChart("Conversion Rate", "Trial conversion rate over time.", "%", [44, 43, 45, 46, 44, 42, 41, 40, 39, 38, 37, 39, 41, 42]),
  churn: makeChart("Churn", "Churn signal over time.", "%", [3.2, 3.4, 3.1, 3.0, 3.5, 3.7, 3.8, 4.0, 4.1, 4.2, 4.0, 3.9, 3.8, 3.7]),
  customers_new: makeChart("New Customers", "New customers over time.", "#", [40, 44, 38, 52, 60, 65, 70, 72, 68, 64, 61, 66, 69, 74]),
  trials: makeChart("Trials", "Trial starts over time.", "#", [18, 19, 20, 22, 25, 28, 29, 31, 30, 32, 33, 31, 30, 34]),
};
