"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { TopNavBar } from "@/components/shared/TopNavBar";
import { Loader2, CheckCircle } from "lucide-react";
import { useResumeParsing } from "@/components/hooks/useResumeParsing";

const STEPS = [
  { key: "extracting", label: "Extracting text from document" },
  { key: "sections", label: "Detecting resume sections" },
  { key: "parsing", label: "AI analyzing your resume" },
  { key: "normalizing", label: "Normalizing skills" },
  { key: "matching", label: "Building match profile" },
];

export default function ParsingLoadingPage() {
  const router = useRouter();
  const { progress, currentStep, isComplete, error, startListening } = useResumeParsing();

  useEffect(() => {
    startListening();
  }, [startListening]);

  useEffect(() => {
    if (isComplete) {
      const timer = setTimeout(() => router.push("/profile/confirm"), 1500);
      return () => clearTimeout(timer);
    }
  }, [isComplete, router]);

  const getStepStatus = (stepKey: string) => {
    if (!currentStep) return "waiting";
    const stepIndex = STEPS.findIndex(s => s.key === stepKey);
    const currentIndex = STEPS.findIndex(s => s.key === currentStep.step);
    if (stepIndex < currentIndex) return "done";
    if (stepIndex === currentIndex) return currentStep.status;
    return "waiting";
  };

  return (
    <div className="flex min-h-screen flex-col">
      <TopNavBar activeTab="jobs" />
      <main className="flex-grow bg-[#F3F2EF] px-4 py-24">
        <div className="mx-auto max-w-xl text-center space-y-12">

          <div className="space-y-4">
            <h1 className="text-3xl font-bold tracking-tight text-foreground">Analyzing Your Resume</h1>
            <p className="text-text-muted">Our AI is extracting and mapping your professional experience.</p>
          </div>

          <div className="rounded-xl border border-gray-200 bg-surface p-8 shadow-sm">
            <div className="flex flex-col gap-6 text-left">
              {STEPS.map(step => {
                const status = getStepStatus(step.key);
                return (
                  <div key={step.key} className={`flex items-center gap-4 ${
                    status === "done" ? "text-emerald-solid" :
                    status === "in_progress" ? "text-primary" :
                    status === "error" ? "text-red-500" :
                    "text-gray-400"
                  }`}>
                    {status === "done" ? (
                      <CheckCircle className="h-6 w-6" />
                    ) : status === "in_progress" ? (
                      <Loader2 className="h-6 w-6 animate-spin" />
                    ) : status === "error" ? (
                      <div className="h-6 w-6 rounded-full border-2 border-red-300 flex items-center justify-center text-xs">!</div>
                    ) : (
                      <div className="h-6 w-6 rounded-full border-2 border-gray-200"></div>
                    )}
                    <span className={`font-medium ${status === "in_progress" ? "animate-pulse" : ""}`}>{step.label}</span>
                  </div>
                );
              })}
            </div>

            <div className="mt-10 mb-2 h-2 w-full overflow-hidden rounded-full bg-gray-100">
              <div
                className="h-full bg-gradient-to-r from-primary to-[var(--color-primary-container)] rounded-full transition-all duration-500"
                style={{ width: `${Math.min(progress, 100)}%` }}
              ></div>
            </div>
            <p className="text-xs text-right text-text-muted">{progress}% Complete</p>

            {error && (
              <p className="mt-4 text-sm text-red-500 text-center">{error}</p>
            )}
          </div>

        </div>
      </main>
    </div>
  );
}
