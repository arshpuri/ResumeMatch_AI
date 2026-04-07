import { TopNavBar } from "@/components/shared/TopNavBar";
import { DASHBOARD_STATS } from "@/data/mockData";

export default function DashboardPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <TopNavBar activeTab="dashboard" />
      <main className="flex-grow bg-[#F3F2EF] px-4 py-8">
        <div className="mx-auto max-w-7xl space-y-8">
          
          {/* Hero Metric Row */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-surface rounded-xl p-6 shadow-sm flex flex-col gap-2">
              <span className="text-sm font-medium text-text-muted">Total Parses</span>
              <span className="text-3xl font-bold text-foreground">{DASHBOARD_STATS.totalParses}</span>
            </div>
            <div className="bg-surface rounded-xl p-6 shadow-sm flex flex-col gap-2">
              <span className="text-sm font-medium text-text-muted">Job Matches Found</span>
              <span className="text-3xl font-bold text-primary">{DASHBOARD_STATS.jobsMatched.toLocaleString()}</span>
            </div>
            <div className="bg-surface rounded-xl p-6 shadow-sm flex flex-col gap-2">
              <span className="text-sm font-medium text-text-muted">Interviews Secured</span>
              <span className="text-3xl font-bold text-[var(--color-emerald-solid)]">{DASHBOARD_STATS.interviewsSecured}</span>
            </div>
            <div className="bg-surface rounded-xl p-6 shadow-sm flex flex-col gap-2">
              <span className="text-sm font-medium text-text-muted">Profile Search Appearances</span>
              <span className="text-3xl font-bold text-foreground">{DASHBOARD_STATS.profileAppearances}</span>
            </div>
          </div>

          {/* Main Chart Area */}
          <div className="bg-surface rounded-xl p-8 shadow-sm">
            <h2 className="text-xl font-bold text-foreground mb-6">Match Trend Over Time</h2>
            <div className="w-full h-64 border-b border-l border-gray-200 relative">
               {/* Mock Line Chart */}
               <svg className="h-full w-full overflow-visible" preserveAspectRatio="none" viewBox="0 0 100 100">
                 <path d="M 0,80 Q 25,70 50,40 T 100,10" fill="none" stroke="var(--color-primary)" strokeWidth="3" vectorEffect="non-scaling-stroke" />
               </svg>
               <div className="absolute -bottom-6 left-0 right-0 flex justify-between text-xs font-medium text-gray-400">
                 <span>Jan</span><span>Feb</span><span>Mar</span><span>Apr</span>
               </div>
               <div className="absolute left-0 bottom-0 top-0 -ml-10 flex flex-col justify-between text-xs font-medium text-gray-400 items-end py-2">
                 <span>100%</span><span>50%</span><span>0%</span>
               </div>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="bg-surface rounded-xl shadow-sm overflow-hidden">
            <div className="px-6 py-5 border-b border-gray-100">
              <h2 className="text-lg font-bold text-foreground">Recent Activity</h2>
            </div>
            <ul className="divide-y divide-gray-100">
              {DASHBOARD_STATS.recentActivity.map(act => (
                <li key={act.id} className="px-6 py-4 flex justify-between hover:bg-gray-50 transition-colors">
                  <span className="text-sm font-medium text-foreground">{act.action}</span>
                  <span className="text-xs text-text-muted">{act.time}</span>
                </li>
              ))}
            </ul>
          </div>

        </div>
      </main>
    </div>
  );
}
