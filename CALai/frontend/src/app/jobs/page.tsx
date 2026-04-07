import { TopNavBar } from "@/components/shared/TopNavBar";
import { JobCard } from "@/components/shared/JobCard";
import { Button } from "@/components/shared/Button";
import { JOB_MATCHES, USER_PROFILE } from "@/data/mockData";
import { Briefcase, SlidersHorizontal, UserCircle2 } from "lucide-react";

export default function JobsFeedPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <TopNavBar activeTab="jobs" />
      <main className="flex-grow bg-[#F3F2EF] px-4 py-8">
        <div className="mx-auto max-w-6xl grid grid-cols-1 lg:grid-cols-4 gap-8">
          
          {/* Left Sidebar: Profile Snippet */}
          <div className="hidden lg:block lg:col-span-1">
            <div className="rounded-xl bg-surface shadow-sm border border-transparent flex flex-col items-center p-6 text-center">
               <div className="h-20 w-20 rounded-full bg-gray-200 overflow-hidden mb-4 border-2 border-white shadow-md">
                 <div className="flex h-full w-full items-center justify-center bg-gray-300 text-3xl font-bold text-gray-600">{USER_PROFILE.name.charAt(0)}</div>
               </div>
               <h3 className="font-bold text-lg text-foreground">{USER_PROFILE.name}</h3>
               <p className="text-sm text-text-muted">{USER_PROFILE.headline}</p>
               <hr className="w-full my-4 border-gray-100" />
               <div className="w-full flex justify-between text-sm">
                 <span className="text-gray-500">Profile matches</span>
                 <span className="font-bold text-primary">45</span>
               </div>
            </div>
          </div>

          {/* Main Feed: Job Listings */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center justify-between mb-2">
              <h2 className="text-xl font-bold text-foreground">Recommended for you</h2>
              <Button variant="tertiary" size="sm" className="gap-2"><SlidersHorizontal className="h-4 w-4" /> Filters</Button>
            </div>
            
            <div className="flex flex-col gap-4">
              {JOB_MATCHES.map((job) => (
                <JobCard key={job.id} job={job} />
              ))}
            </div>
          </div>

          {/* Right Sidebar: Contextual Prompts */}
          <div className="hidden lg:block lg:col-span-1 space-y-4">
             <div className="rounded-xl bg-surface p-5 shadow-sm border border-transparent">
                <h3 className="font-bold text-sm text-foreground mb-3 flex items-center gap-2">
                  <Briefcase className="h-4 w-4 text-primary" /> Premium Insights
                </h3>
                <p className="text-xs text-text-muted mb-4">Adding &quot;GraphQL&quot; to your profile could unlock 12% more senior roles in your area.</p>
                <Button variant="outline" size="sm" className="w-full">Update Profile</Button>
             </div>
          </div>

        </div>
      </main>
    </div>
  );
}
