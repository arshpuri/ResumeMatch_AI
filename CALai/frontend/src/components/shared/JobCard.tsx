"use client";

import React, { useState } from "react";
import Link from "next/link";
import { MapPin, Clock, Bookmark, BookmarkCheck } from "lucide-react";
import { type JobMatch } from "@/lib/api";
import { MatchScore } from "./MatchScore";
import { Button } from "./Button";
import { api } from "@/lib/api";

export const JobCard = ({ job }: { job: JobMatch }) => {
  const [saving, setSaving] = useState(false);
  const [applying, setApplying] = useState(false);
  const [applied, setApplied] = useState(false);

  const handleSave = async (e: React.MouseEvent) => {
    e.preventDefault();
    setSaving(true);
    try { await api.jobs.save(job.id); } catch { /* ignore */ }
    finally { setSaving(false); }
  };

  const handleApply = async (e: React.MouseEvent) => {
    e.preventDefault();
    setApplying(true);
    try { await api.jobs.apply(job.id); setApplied(true); }
    catch { setApplied(true); }
    finally { setApplying(false); }
  };

  return (
    <div className="flex flex-col gap-4 rounded-xl bg-surface p-6 shadow-sm border border-transparent transition-all hover:border-[var(--color-primary-fixed-dim)] hover:shadow-md">
      <div className="flex items-start justify-between">
        <div>
          <Link href={`/jobs/${job.id}`} className="text-xl font-semibold text-foreground hover:text-primary transition-colors">
            {job.title}
          </Link>
          <div className="mt-1 flex items-center gap-2 text-sm text-text-muted">
            <span className="font-medium text-foreground">{job.company}</span>
            <span>&bull;</span>
            <span className="flex items-center gap-1"><MapPin className="h-3 w-3" /> {job.location}</span>
            {job.salary && <><span>&bull;</span><span className="text-emerald-600 font-medium">{job.salary}</span></>}
          </div>
        </div>
        <MatchScore score={job.matchScore} size="lg" />
      </div>

      <div className="flex flex-wrap gap-2 mt-2">
        {job.reasons.map((reason, idx) => (
          <span key={idx} className="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10">
            ✓ {reason}
          </span>
        ))}
      </div>

      <div className="mt-4 flex items-center justify-between border-t border-gray-100 pt-4">
        <div className="flex items-center gap-1 text-xs text-gray-400">
          <Clock className="h-3 w-3" /> {job.postedAt}
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={handleSave} disabled={saving}>
            <Bookmark className="h-3.5 w-3.5 mr-1" /> Save
          </Button>
          <Button variant="primary" size="sm" onClick={handleApply} disabled={applying || applied}>
            {applied ? "✓ Applied" : "Quick Apply"}
          </Button>
        </div>
      </div>
    </div>
  );
};
