"use client";

import { useState, useEffect } from "react";
import { TopNavBar } from "@/components/shared/TopNavBar";
import { Button } from "@/components/shared/Button";
import { api, type UserProfile } from "@/lib/api";
import { Pencil, Plus, Loader2 } from "lucide-react";

export default function ProfilePage() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.profile.get()
      .then(setProfile)
      .catch(() => setProfile(null))
      .finally(() => setLoading(false));
  }, []);

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

  const p = profile || { name: "User", headline: "", location: "", status: "Open to Work", completionScore: 0, skills: [], experience: [], education: [] };

  return (
    <div className="flex min-h-screen flex-col">
      <TopNavBar activeTab="profile" />
      <main className="flex-grow bg-[#F3F2EF] px-4 py-8">
        <div className="mx-auto max-w-6xl grid grid-cols-1 md:grid-cols-3 gap-8">

          {/* Main Profile Area */}
          <div className="md:col-span-2 space-y-6">

            {/* Header Card */}
            <div className="rounded-xl bg-surface shadow-sm overflow-hidden relative">
              <div className="h-32 bg-[#E3E2DF] w-full"></div>
              <div className="px-6 pb-6 pt-16 relative">
                 <div className="absolute -top-16 left-6 h-32 w-32 rounded-full bg-white p-1 shadow-sm">
                   <div className="flex h-full w-full items-center justify-center rounded-full bg-gray-200 text-5xl font-bold text-gray-500">{p.name.charAt(0)}</div>
                 </div>

                 <div className="flex justify-between items-start">
                   <div>
                     <h1 className="text-2xl font-bold text-foreground">{p.name}</h1>
                     <p className="text-lg text-text-muted mt-1">{p.headline || "No headline set"}</p>
                     <p className="text-sm text-gray-400 mt-2">{p.location || "No location set"}</p>
                   </div>
                   <Pencil className="h-5 w-5 text-gray-400 cursor-pointer hover:text-primary" />
                 </div>

                 <div className="mt-6">
                   <Button variant="outline" className="font-semibold text-primary border-primary">{p.status}</Button>
                 </div>
              </div>
            </div>

            {/* Experience Card */}
            <div className="rounded-xl bg-surface p-6 shadow-sm">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-foreground">Experience</h2>
                <div className="flex gap-3">
                  <Plus className="h-5 w-5 text-gray-400 cursor-pointer hover:text-primary" />
                  <Pencil className="h-5 w-5 text-gray-400 cursor-pointer hover:text-primary" />
                </div>
              </div>

              {p.experience.length === 0 ? (
                <p className="text-sm text-text-muted">No experience data yet. Upload your resume to auto-populate.</p>
              ) : (
                <div className="space-y-6">
                  {p.experience.map(exp => (
                    <div key={exp.id} className="border-b border-gray-100 last:border-0 pb-6 last:pb-0">
                      <h3 className="font-bold text-foreground">{exp.role}</h3>
                      <p className="text-sm text-text-muted">{exp.company}</p>
                      <p className="text-xs text-gray-400 mt-1 mb-3">{exp.period}</p>
                      <ul className="list-disc pl-5 text-sm text-foreground/80 space-y-1">
                        {exp.bullets.map((b, i) => <li key={i}>{b}</li>)}
                      </ul>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Education Card */}
            {p.education.length > 0 && (
              <div className="rounded-xl bg-surface p-6 shadow-sm">
                <h2 className="text-xl font-bold text-foreground mb-6">Education</h2>
                <div className="space-y-4">
                  {p.education.map(edu => (
                    <div key={edu.id}>
                      <h3 className="font-bold text-foreground">{edu.degree}</h3>
                      <p className="text-sm text-text-muted">{edu.institution}</p>
                      <p className="text-xs text-gray-400 mt-1">{edu.period}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

          </div>

          {/* Right Sidebar */}
          <div className="md:col-span-1 space-y-6">

            <div className="rounded-xl bg-surface p-6 shadow-sm">
              <h2 className="text-lg font-bold text-foreground mb-4">Profile completion</h2>
              <div className="flex items-center gap-4 mb-4">
                <div className="relative h-16 w-16">
                  <svg className="h-full w-full" viewBox="0 0 36 36">
                    <path className="text-gray-200" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="4" />
                    <path className="text-primary" strokeDasharray={`${p.completionScore}, 100`} d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="4" />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center text-xs font-bold">{p.completionScore}%</div>
                </div>
                <p className="text-sm text-text-muted">
                  {p.completionScore >= 100 ? "Profile complete!" : "Upload resume & add details to reach 100%"}
                </p>
              </div>
              <Button variant="outline" className="w-full">Add section</Button>
            </div>

            <div className="rounded-xl bg-surface p-6 shadow-sm">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-bold text-foreground">Skills</h2>
                <Pencil className="h-4 w-4 text-gray-400 cursor-pointer hover:text-primary" />
              </div>
              {p.skills.length === 0 ? (
                <p className="text-sm text-text-muted">No skills yet. Upload your resume!</p>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {p.skills.map((skill, idx) => (
                    <span key={skill} className={`inline-flex items-center rounded-full px-3 py-1 text-sm font-medium ${idx < 5 ? 'bg-primary text-white' : 'bg-transparent text-foreground ring-1 ring-inset ring-gray-300'}`}>
                      {skill}
                    </span>
                  ))}
                </div>
              )}
            </div>

          </div>

        </div>
      </main>
    </div>
  );
}
