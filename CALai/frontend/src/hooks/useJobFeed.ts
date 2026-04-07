/**
 * useJobFeed — paginated job feed hook with loading states.
 */

"use client";

import { useState, useEffect, useCallback } from "react";
import { api, type JobMatch, type JobFeedResponse } from "@/lib/api";

export function useJobFeed() {
  const [jobs, setJobs] = useState<JobMatch[]>([]);
  const [nextCursor, setNextCursor] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchFeed = useCallback(async (cursor?: string) => {
    try {
      setIsLoading(true);
      setError(null);
      const data: JobFeedResponse = await api.jobs.getFeed(cursor);
      if (cursor) {
        setJobs((prev) => [...prev, ...data.jobs]);
      } else {
        setJobs(data.jobs);
      }
      setNextCursor(data.nextCursor);
      setTotal(data.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load jobs");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchFeed();
  }, [fetchFeed]);

  const loadMore = useCallback(() => {
    if (nextCursor) fetchFeed(nextCursor);
  }, [nextCursor, fetchFeed]);

  const refresh = useCallback(() => fetchFeed(), [fetchFeed]);

  return { jobs, isLoading, error, total, hasMore: !!nextCursor, loadMore, refresh };
}
