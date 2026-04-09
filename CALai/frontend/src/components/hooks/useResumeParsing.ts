/**
 * useResumeParsing — SSE connection hook for parsing progress.
 */

"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { getAccessToken } from "@/lib/api";

interface ParsingStep {
  step: string;
  progress: number;
  status: string;
  message?: string;
}

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export function useResumeParsing() {
  const [steps, setSteps] = useState<ParsingStep[]>([]);
  const [currentStep, setCurrentStep] = useState<ParsingStep | null>(null);
  const [progress, setProgress] = useState(0);
  const [isComplete, setIsComplete] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  const startListening = useCallback(() => {
    // Close any existing connection
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    const token = getAccessToken();
    // EventSource doesn't support custom headers, so we pass token as query param
    const url = `${BACKEND_URL}/api/v1/resume/parsing-status?token=${token || ""}`;
    const es = new EventSource(url);
    eventSourceRef.current = es;

    es.onmessage = (event) => {
      try {
        const data: ParsingStep = JSON.parse(event.data);
        setSteps((prev) => [...prev, data]);
        setCurrentStep(data);
        setProgress(data.progress);

        if (data.status === "error") {
          setError(data.message || "Parsing error");
          es.close();
        }

        if (data.progress >= 100 || data.step === "complete") {
          setIsComplete(true);
          es.close();
        }
      } catch {
        // Ignore parse errors
      }
    };

    es.onerror = () => {
      setError("Connection lost. Parsing may still be in progress.");
      es.close();
    };
  }, []);

  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  return { steps, currentStep, progress, isComplete, error, startListening };
}
