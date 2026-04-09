"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { TopNavBar } from "@/components/shared/TopNavBar";
import { Button } from "@/components/shared/Button";
import { api, type UserProfile } from "@/lib/api";
import { PencilLine, ShieldCheck, Loader2 } from "lucide-react";

export default function ProfileConfirmPage() {
  const router = useRouter();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.profile.get()
      .then(setProfile)
      .catch(() => setProfile(null))
      .finally(() => setLoading(false));
  }, []);

  const handleConfirm = () => {
    router.push("/jobs");
  };

  if (loading) {
    return (
      <div className="flex min-h-screen flex-col">
        <TopNavBar activeTab="profile" />
        <main className="flex-grow bg-[#F3F2EF] flex items-center justify-center">
          <Loader2 className="h-8 w-8 text-primary animate-spin" />
        </main>
      </div>
    );
  }

  const p = profile || { name: "User", headline: "", skills: [], location: "", status: "", completionScore: 0, experience: [], education: [] };

  return (
    <div className="flex min-h-screen flex-col">
      <TopNavBar activeTab="profile" />
      <main className="flex-grow bg-[#F3F2EF] px-4 py-8">
        <div className="mx-auto max-w-4xl space-y-6">

          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-foreground">Review your profile</h1>
              <p className="text-text-muted">We extracted this from your resume. Edit any errors to ensure perfect matches.</p>
            </div>
            <Button variant="primary" onClick={handleConfirm}>Confirm &amp; Continue</Button>
          </div>

          <div className="rounded-xl border border-gray-200 bg-surface p-8 shadow-sm">
            <div className="mb-6 flex items-center gap-2 text-primary font-medium border-b border-gray-100 pb-4">
              <ShieldCheck className="h-5 w-5" />
              <span>Parsed successfully</span>
            </div>

            <div className="grid gap-8 md:grid-cols-2">
              <div className="space-y-4">
                <div>
                  <label className="text-xs font-semibold text-text-muted uppercase tracking-wider">Full Name</label>
                  <div className="mt-1 flex justify-between items-center bg-gray-50 p-3 rounded-md ring-1 ring-inset ring-gray-200">
                    <span className="font-medium text-foreground">{p.name}</span>
                    <PencilLine className="h-4 w-4 text-gray-400 cursor-pointer hover:text-primary" />
                  </div>
                </div>
                <div>
                  <label className="text-xs font-semibold text-text-muted uppercase tracking-wider">Professional Headline</label>
                  <div className="mt-1 flex justify-between items-center bg-gray-50 p-3 rounded-md ring-1 ring-inset ring-gray-200">
                    <span className="font-medium text-foreground">{p.headline || "Not detected"}</span>
                    <PencilLine className="h-4 w-4 text-gray-400 cursor-pointer hover:text-primary" />
                  </div>
                </div>
                <div>
                  <label className="text-xs font-semibold text-text-muted uppercase tracking-wider">Location</label>
                  <div className="mt-1 flex justify-between items-center bg-gray-50 p-3 rounded-md ring-1 ring-inset ring-gray-200">
                    <span className="font-medium text-foreground">{p.location || "Not detected"}</span>
                    <PencilLine className="h-4 w-4 text-gray-400 cursor-pointer hover:text-primary" />
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <label className="text-xs font-semibold text-text-muted uppercase tracking-wider">Extracted Skills</label>
                <div className="flex flex-wrap gap-2 p-3 bg-gray-50 rounded-md ring-1 ring-inset ring-gray-200">
                  {p.skills.length === 0 ? (
                    <span className="text-sm text-text-muted">No skills detected</span>
                  ) : (
                    p.skills.map(skill => (
                      <span key={skill} className="inline-flex items-center rounded-md bg-[var(--color-primary-fixed)] px-2 py-1 text-xs font-medium text-[var(--color-on-primary-fixed)] ring-1 ring-inset ring-primary/20">
                        {skill} <button className="ml-1 text-[var(--color-on-primary-fixed)] opacity-50 hover:opacity-100">&times;</button>
                      </span>
                    ))
                  )}
                  <button className="text-xs text-primary font-medium hover:underline">+ Add skill</button>
                </div>
              </div>
            </div>

          </div>

        </div>
      </main>
    </div>
  );
}
