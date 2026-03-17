import { generateGrowthBrief } from "@/lib/brief";
import { mockCharts, mockOverview } from "@/lib/mock-data";
import { getChart, getOverview, hasRevenueCatKey } from "@/lib/revenuecat";

const PROJECT_ID = process.env.REVENUECAT_PROJECT_ID || "proj058a6330";
const LIVE_CHARTS = ["revenue", "mrr", "trial_conversion_rate", "churn", "customers_new", "trials"] as const;
const SUPPORTING_CHARTS = ["revenue", "mrr", "trial_conversion_rate", "churn"] as const;

function currency(value: number) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(value);
}

function compactNumber(value: number) {
  return new Intl.NumberFormat("en-US", { notation: "compact", maximumFractionDigits: 1 }).format(value);
}

function miniSeries(values: number[]) {
  const max = Math.max(...values, 1);
  return values
    .map((value, index) => {
      const x = (index / Math.max(values.length - 1, 1)) * 100;
      const y = 100 - (value / max) * 100;
      return `${x},${y}`;
    })
    .join(" ");
}

export default async function Home() {
  const useMock = !hasRevenueCatKey();

  const overview = useMock ? mockOverview : await getOverview(PROJECT_ID);
  const chartResponses = useMock
    ? LIVE_CHARTS.map((name) => mockCharts[name])
    : await Promise.all(LIVE_CHARTS.map((chart) => getChart(PROJECT_ID, chart)));

  const chartMap = Object.fromEntries(LIVE_CHARTS.map((name, i) => [name, chartResponses[i]]));
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

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-50">
      <nav className="sticky top-0 z-50 border-b border-zinc-800 bg-zinc-950/90 backdrop-blur-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-3 lg:px-10">
          <span className="text-sm font-semibold text-teal-400">Kit&apos;s Take-Home Submission</span>
          <div className="flex gap-4 text-sm">
            <a href="https://github.com/KitTheRevenueCat/revenuecat-growth-brief" target="_blank" rel="noopener" className="text-zinc-400 hover:text-teal-300 transition">Repo</a>
            <a href="blog.html" className="text-zinc-400 hover:text-teal-300 transition">Blog</a>
            <a href="video.html" className="text-zinc-400 hover:text-teal-300 transition">Video</a>
            <a href="social.html" className="text-zinc-400 hover:text-teal-300 transition">Social</a>
            <a href="campaign.html" className="text-zinc-400 hover:text-teal-300 transition">Campaign</a>
            <a href="process.html" className="text-zinc-400 hover:text-teal-300 transition">Process</a>
          </div>
        </div>
      </nav>
      <div className="mx-auto flex max-w-7xl flex-col gap-10 px-6 py-10 lg:px-10">
        <section className="rounded-3xl border border-zinc-800 bg-zinc-900/70 p-8 shadow-2xl shadow-black/20">
          <div className="mb-8 flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div className="max-w-3xl">
              <p className="mb-3 text-sm font-medium uppercase tracking-[0.2em] text-teal-400">RevenueCat Charts API take-home</p>
              <h1 className="text-4xl font-semibold tracking-tight lg:text-5xl">RevenueCat Growth Brief</h1>
              <p className="mt-4 text-lg leading-8 text-zinc-300">
                A brief-first monetization operator that turns RevenueCat Charts API data into a ranked weekly investigation brief. The shell exists to support decisions, not replace the dashboard.
              </p>
              <p className="mt-3 max-w-2xl text-sm leading-6 text-zinc-400">{brief.summary}</p>
            </div>
            <div className="space-y-3">
              <div className="rounded-2xl border border-zinc-800 bg-zinc-950/60 px-4 py-3 text-sm text-zinc-300">
                <div className="font-medium text-zinc-100">Comparison windows</div>
                <div>Last 7 data points vs the prior 7 data points</div>
              </div>
              <div className="rounded-2xl border border-zinc-800 bg-zinc-950/60 px-4 py-3 text-sm text-zinc-300">
                <div className="font-medium text-zinc-100">Mode</div>
                <div>{useMock ? "Mock data — hosted demo is intentionally synthetic. Live findings cited elsewhere come from a local run against the provided Dark Noise project." : "Live RevenueCat project data"}</div>
              </div>
            </div>
          </div>

          <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
            <div className="rounded-3xl border border-zinc-800 bg-zinc-950/60 p-6">
              <div className="mb-4 flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium uppercase tracking-[0.2em] text-teal-400">Weekly operator brief</p>
                  <h2 className="mt-2 text-2xl font-semibold">What needs attention this week</h2>
                </div>
                <div className="rounded-full border border-teal-500/30 bg-teal-500/10 px-3 py-1 text-sm text-teal-300">Deterministic</div>
              </div>
              <div className="space-y-4">
                {brief.sections.map((section, index) => (
                  <div key={section.title} className="rounded-2xl border border-zinc-800 bg-zinc-900/70 p-4">
                    <div className="mb-2 text-xs font-medium uppercase tracking-[0.18em] text-zinc-500">Priority {index + 1}</div>
                    <h3 className="text-lg font-semibold text-zinc-100">{section.title}</h3>
                    <p className="mt-2 text-sm leading-6 text-zinc-300">{section.summary}</p>
                    <p className="mt-3 text-sm leading-6 text-zinc-500"><span className="font-medium text-zinc-400">Evidence:</span> {section.evidence}</p>
                    <p className="mt-3 text-sm leading-6 text-teal-200"><span className="font-medium text-teal-300">Investigate next:</span> {section.action}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-1">
              {brief.kpis.map((kpi) => (
                <div key={kpi.label} className="rounded-2xl border border-zinc-800 bg-zinc-950/60 p-4">
                  <div className="text-sm text-zinc-400">{kpi.label}</div>
                  <div className="mt-2 text-3xl font-semibold text-zinc-100">{kpi.value}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section>
          <div className="mb-4 flex items-end justify-between">
            <div>
              <p className="text-sm font-medium uppercase tracking-[0.2em] text-teal-400">Supporting evidence</p>
              <h2 className="mt-2 text-2xl font-semibold">Charts that back the brief</h2>
            </div>
          </div>
          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
            {SUPPORTING_CHARTS.map((key) => {
              const chart = chartMap[key];
              const series = chart.values.filter((v) => v.measure === 0 && !v.incomplete).slice(-12);
              const values = series.map((point) => point.value);
              const latest = values.at(-1) ?? 0;
              const total = chart.summary?.total?.[chart.measures[0]?.display_name] ?? latest;
              const isMoney = chart.measures[0]?.unit === "$";
              return (
                <article key={key} className="rounded-3xl border border-zinc-800 bg-zinc-900/70 p-5">
                  <h3 className="text-lg font-semibold text-zinc-100">{chart.display_name}</h3>
                  <p className="mt-1 text-sm leading-6 text-zinc-400">{chart.description}</p>
                  <div className="mt-4 mb-4 flex items-end justify-between">
                    <div>
                      <div className="text-sm text-zinc-500">Latest point</div>
                      <div className="text-2xl font-semibold">{isMoney ? currency(latest) : compactNumber(latest)}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-zinc-500">Summary total</div>
                      <div className="text-lg text-zinc-300">{isMoney ? currency(total) : compactNumber(total)}</div>
                    </div>
                  </div>
                  <div className="rounded-2xl border border-zinc-800 bg-zinc-950/60 p-3">
                    <svg viewBox="0 0 100 100" className="h-24 w-full overflow-visible">
                      <polyline fill="none" stroke="rgb(45 212 191)" strokeWidth="3" points={miniSeries(values.length ? values : [0])} />
                    </svg>
                  </div>
                </article>
              );
            })}
          </div>
        </section>
        <section className="rounded-3xl border border-zinc-800 bg-zinc-900/70 p-8">
          <div className="mb-6">
            <p className="text-sm font-medium uppercase tracking-[0.2em] text-teal-400">Submission package</p>
            <h2 className="mt-2 text-2xl font-semibold">All deliverables</h2>
          </div>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            <a href="https://github.com/KitTheRevenueCat/revenuecat-growth-brief" target="_blank" rel="noopener" className="rounded-2xl border border-zinc-800 bg-zinc-950/60 p-4 transition hover:border-teal-500/50">
              <div className="text-sm text-teal-400">Tool / Resource</div>
              <div className="mt-1 text-lg font-semibold text-zinc-100">GitHub Repo</div>
              <div className="mt-2 text-sm text-zinc-400">Source code, README, architecture docs</div>
            </a>
            <a href="blog.html" className="rounded-2xl border border-zinc-800 bg-zinc-950/60 p-4 transition hover:border-teal-500/50">
              <div className="text-sm text-teal-400">Blog Post</div>
              <div className="mt-1 text-lg font-semibold text-zinc-100">Launch Announcement</div>
              <div className="mt-2 text-sm text-zinc-400">Launch post + full technical write-up on GitHub</div>
            </a>
            <a href="video.html" className="rounded-2xl border border-zinc-800 bg-zinc-950/60 p-4 transition hover:border-teal-500/50">
              <div className="text-sm text-teal-400">Video Tutorial</div>
              <div className="mt-1 text-lg font-semibold text-zinc-100">94-Second Walkthrough</div>
              <div className="mt-2 text-sm text-zinc-400">Screen recording with ElevenLabs v3 voiceover</div>
            </a>
            <a href="social.html" className="rounded-2xl border border-zinc-800 bg-zinc-950/60 p-4 transition hover:border-teal-500/50">
              <div className="text-sm text-teal-400">Social Posts</div>
              <div className="mt-1 text-lg font-semibold text-zinc-100">5 Posts for X</div>
              <div className="mt-2 text-sm text-zinc-400">Copy + media assets for each post</div>
            </a>
            <a href="campaign.html" className="rounded-2xl border border-zinc-800 bg-zinc-950/60 p-4 transition hover:border-teal-500/50">
              <div className="text-sm text-teal-400">Growth Campaign</div>
              <div className="mt-1 text-lg font-semibold text-zinc-100">Campaign Plan + Early Receipts</div>
              <div className="mt-2 text-sm text-zinc-400">Target communities, budget, measurement framework, live post links</div>
            </a>
            <a href="process.html" className="rounded-2xl border border-zinc-800 bg-zinc-950/60 p-4 transition hover:border-teal-500/50">
              <div className="text-sm text-teal-400">Process Log</div>
              <div className="mt-1 text-lg font-semibold text-zinc-100">How I Built This</div>
              <div className="mt-2 text-sm text-zinc-400">Decisions, tradeoffs, tools, timeline</div>
            </a>
          </div>
        </section>
      </div>
    </main>
  );
}
