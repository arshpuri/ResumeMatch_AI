"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { TopNavBar } from "@/components/shared/TopNavBar";
import { MatchScore } from "@/components/shared/MatchScore";
import { Button } from "@/components/shared/Button";
import { api, type JobDetail } from "@/lib/api";
import { MapPin, Building, AlertCircle, Loader2, Bookmark, BookmarkCheck } from "lucide-react";

export default function JobDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [job, setJob] = useState<JobDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [applying, setApplying] = useState(false);
  const [applied, setApplied] = useState(false);

  useEffect(() => {
    if (!id) return;
    api.jobs.getDetail(id)
      .then(setJob)
      .catch(() => setJob(null))
      .finally(() => setLoading(false));
  }, [id]);

  const handleSave = async () => {
    if (!job) return;
    setSaving(true);
    try {
      if (job.isSaved) {
        await api.jobs.unsave(job.id);
        setJob({ ...job, isSaved: false });
      } else {
        await api.jobs.save(job.id);
        setJob({ ...job, isSaved: true });
      }
    } catch (err) { /* ignore */ }
    finally { setSaving(false); }
  };

  const handleApply = async () => {
    if (!job) return;
    setApplying(true);
    try {
      await api.jobs.apply(job.id);
      setApplied(true);
    } catch (err: any) {
      if (err?.body?.includes("Already")) setApplied(true);
    } finally { setApplying(false); }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen flex-col">
        <TopNavBar activeTab="jobs" />
        <main className="flex-grow bg-[#F3F2EF] flex items-center justify-center">
          <Loader2 className="h-8 w-8 text-primary animate-spin" />
        </main>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="flex min-h-screen flex-col">
        <TopNavBar activeTab="jobs" />
        <main className="flex-grow bg-[#F3F2EF] flex items-center justify-center">
          <p className="text-text-muted">Job not found.</p>
        </main>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col">
      <TopNavBar activeTab="jobs" />
      <main className="flex-grow bg-[#F3F2EF] px-4 py-8">
        <div className="mx-auto max-w-6xl">

          <div className="mb-4">
            <Link href="/jobs" className="text-sm font-medium text-primary hover:underline">&larr; Back to jobs</Link>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

            {/* Left Main Column: Job Details */}
            <div className="lg:col-span-2 space-y-6">
              <div className="rounded-xl bg-surface p-8 shadow-sm">
                <h1 className="text-3xl font-bold tracking-tight text-foreground mb-4">{job.title}</h1>
                <div className="flex items-center gap-4 text-text-muted font-medium mb-6">
                  <span className="flex items-center gap-1"><Building className="h-4 w-4" /> {job.company}</span>
                  <span className="flex items-center gap-1"><MapPin className="h-4 w-4" /> {job.location}</span>
                  {job.salary && <span className="text-sm text-emerald-600 font-semibold">{job.salary}</span>}
                </div>

                <div className="flex gap-3 pb-8 border-b border-gray-100">
                  <Button variant="primary" size="lg" onClick={handleApply} disabled={applying || applied}>
                    {applied ? "✓ Applied" : applying ? "Applying..." : "Apply Now"}
                  </Button>
                  <Button variant="outline" size="lg" onClick={handleSave} disabled={saving}>
                    {job.isSaved ? <><BookmarkCheck className="h-4 w-4 mr-1" /> Saved</> : <><Bookmark className="h-4 w-4 mr-1" /> Save</>}
                  </Button>
                </div>

                <div className="mt-8 space-y-8 text-foreground/80 leading-relaxed">
                  {job.description && (
                    <section>
                      <h2 className="text-xl font-bold text-foreground mb-3">About the Role</h2>
                      <p>{job.description}</p>
                    </section>
                  )}
                  {job.responsibilities && job.responsibilities.length > 0 && (
                    <section>
                      <h2 className="text-xl font-bold text-foreground mb-3">Key Responsibilities</h2>
                      <ul className="list-disc pl-5 space-y-2">
                        {job.responsibilities.map((r, i) => <li key={i}>{r}</li>)}
                      </ul>
                    </section>
                  )}
                </div>
              </div>
            </div>

            {/* Right Sidebar: AI Match Analysis */}
            <div className="lg:col-span-1 space-y-6">
              <div className="rounded-xl bg-surface p-6 shadow-sm border-t-4 border-[var(--color-emerald-solid)]">
                <h3 className="font-bold text-lg text-foreground flex justify-between items-center mb-6">
                  AI Match Analysis
                  <MatchScore score={job.matchScore} size="lg" />
                </h3>

                <div className="space-y-4">
                  <div>
                    <h4 className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2">Why you match</h4>
                    <ul className="space-y-2">
                      {job.reasons.map((reason, idx) => (
                        <li key={idx} className="flex items-start gap-2 text-sm text-foreground">
                          <span className="text-[var(--color-emerald-solid)] mt-0.5">✔</span> {reason}
                        </li>
                      ))}
                    </ul>
                  </div>

                  {job.missingSkills.length > 0 && (
                    <div className="pt-4 border-t border-gray-100">
                      <h4 className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2 flex items-center gap-1">
                        <AlertCircle className="h-3 w-3 text-amber-500" /> Missing Skills
                      </h4>
                      <ul className="space-y-2">
                        {job.missingSkills.map((skill, idx) => (
                          <li key={idx} className="flex items-start gap-2 text-sm text-foreground">
                            <span className="text-amber-500 mt-0.5">⚠</span> {skill} not found in resume
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                <div className="mt-8 pt-4 border-t border-gray-100 text-center">
                  <Link href="/profile" className="text-sm text-primary font-medium hover:underline">Edit Profile to add missing skills</Link>
                </div>
              </div>
            </div>

          </div>
        </div>
      </main>
    </div>
  );
}
