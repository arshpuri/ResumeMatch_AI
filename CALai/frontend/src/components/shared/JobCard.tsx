import React from "react";
import Link from "next/link";
import { MapPin, Clock } from "lucide-react";
import { type JobMatch } from "@/data/mockData";
import { MatchScore } from "./MatchScore";
import { Button } from "./Button";

export const JobCard = ({ job }: { job: JobMatch }) => {
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
          <Button variant="outline" size="sm">Save</Button>
          <Button variant="primary" size="sm">Quick Apply</Button>
        </div>
      </div>
    </div>
  );
};
