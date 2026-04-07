import { TopNavBar } from "@/components/shared/TopNavBar";
import { MatchScore } from "@/components/shared/MatchScore";
import { Button } from "@/components/shared/Button";
import { JOB_MATCHES } from "@/data/mockData";
import { MapPin, Building, AlertCircle } from "lucide-react";
import Link from "next/link";

export default async function JobDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params;
  const job = JOB_MATCHES.find(j => j.id === id) || JOB_MATCHES[0];

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
                </div>
                
                <div className="flex gap-3 pb-8 border-b border-gray-100">
                  <Button variant="primary" size="lg">Apply Now</Button>
                  <Button variant="outline" size="lg">Save</Button>
                </div>

                <div className="mt-8 space-y-8 text-foreground/80 leading-relaxed">
                  <section>
                    <h2 className="text-xl font-bold text-foreground mb-3">About the Role</h2>
                    <p>We are seeking a highly skilled and experienced professional to join our dynamic team. You will be responsible for building exceptional user experiences...</p>
                  </section>
                  <section>
                    <h2 className="text-xl font-bold text-foreground mb-3">Key Responsibilities</h2>
                    <ul className="list-disc pl-5 space-y-2">
                      <li>Develop and maintain web applications using React.</li>
                      <li>Collaborate with cross-functional teams to define, design, and ship new features.</li>
                    </ul>
                  </section>
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
                  <Button variant="tertiary" className="text-sm">Edit Profile to add missing skills</Button>
                </div>
              </div>
            </div>

          </div>
          
        </div>
      </main>
    </div>
  );
}
