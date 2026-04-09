"use client";

import { useState, useEffect } from "react";
import { TopNavBar } from "@/components/shared/TopNavBar";
import { JobCard } from "@/components/shared/JobCard";
import { Button } from "@/components/shared/Button";
import { api, type JobMatch, type UserProfile } from "@/lib/api";
import { Briefcase, SlidersHorizontal, Loader2 } from "lucide-react";

export default function JobsFeedPage() {
  const [jobs, setJobs] = useState<JobMatch[]>([]);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    Promise.all([
      api.jobs.getFeed().catch(() => ({ jobs: [], nextCursor: null, total: 0 })),
      api.profile.get().catch(() => null),
    ]).then(([feed, prof]) => {
      setJobs(feed.jobs);
      setProfile(prof);
      setLoading(false);
    });
  }, []);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    setLoading(true);
    try {
      const result = await api.jobs.search(searchQuery);
      setJobs(result.jobs);
    } catch {
      // keep existing jobs
    } finally {
      setLoading(false);
    }
  };

  const userName = profile?.name || "User";

  return (
    <div className="flex min-h-screen flex-col">
      <TopNavBar activeTab="jobs" onSearch={handleSearch} searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
      <main className="flex-grow bg-[#F3F2EF] px-4 py-8">
        <div className="mx-auto max-w-6xl grid grid-cols-1 lg:grid-cols-4 gap-8">

          {/* Left Sidebar: Profile Snippet */}
          <div className="hidden lg:block lg:col-span-1">
            <div className="rounded-xl bg-surface shadow-sm border border-transparent flex flex-col items-center p-6 text-center">
               <div className="h-20 w-20 rounded-full bg-gray-200 overflow-hidden mb-4 border-2 border-white shadow-md">
                 <div className="flex h-full w-full items-center justify-center bg-gray-300 text-3xl font-bold text-gray-600">{userName.charAt(0)}</div>
               </div>
               <h3 className="font-bold text-lg text-foreground">{userName}</h3>
               <p className="text-sm text-text-muted">{profile?.headline || "Upload resume to see profile"}</p>
               <hr className="w-full my-4 border-gray-100" />
               <div className="w-full flex justify-between text-sm">
                 <span className="text-gray-500">Profile matches</span>
                 <span className="font-bold text-primary">{jobs.length}</span>
               </div>
            </div>
          </div>

          {/* Main Feed: Job Listings */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center justify-between mb-2">
              <h2 className="text-xl font-bold text-foreground">Recommended for you</h2>
              <Button variant="tertiary" size="sm" className="gap-2"><SlidersHorizontal className="h-4 w-4" /> Filters</Button>
            </div>

            {loading ? (
              <div className="flex flex-col items-center justify-center py-16 gap-4">
                <Loader2 className="h-8 w-8 text-primary animate-spin" />
                <p className="text-sm text-text-muted">Loading personalized matches...</p>
              </div>
            ) : jobs.length === 0 ? (
              <div className="rounded-xl bg-surface p-8 text-center shadow-sm">
                <p className="text-text-muted">No matches found. Upload your resume to see personalized job recommendations!</p>
              </div>
            ) : (
              <div className="flex flex-col gap-4">
                {jobs.map((job) => (
                  <JobCard key={job.id} job={job} />
                ))}
              </div>
            )}
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
