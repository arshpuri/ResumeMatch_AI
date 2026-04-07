import React from "react";
import { cn } from "./Button";

interface MatchScoreProps {
  score: number;
  className?: string;
  size?: "sm" | "md" | "lg";
}

export const MatchScore = ({ score, className, size = "md" }: MatchScoreProps) => {
  let colorClass = "bg-emerald-light text-emerald-solid ring-emerald-light";
  if (score < 70) colorClass = "bg-amber-light text-amber-solid ring-amber-light";
  
  // Actually we mapped CSS variables, so let's use the exact classes
  if (score >= 80) {
    colorClass = "bg-[var(--color-emerald-light)] text-[var(--color-emerald-solid)] ring-[var(--color-emerald-light)]";
  } else if (score >= 50) {
    colorClass = "bg-[var(--color-amber-light)] text-[var(--color-amber-solid)] ring-[var(--color-amber-light)]";
  } else {
    colorClass = "bg-red-50 text-red-700 ring-red-50";
  }

  const sizes = {
    sm: "px-2 py-0.5 text-xs",
    md: "px-2.5 py-0.5 text-sm",
    lg: "px-3 py-1 text-base",
  };

  return (
    <span className={cn("inline-flex items-center rounded-full font-medium ring-1 ring-inset", colorClass, sizes[size], className)}>
      {score}% Match
    </span>
  );
};
