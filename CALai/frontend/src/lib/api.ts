/**
 * API Client — typed fetch wrapper with auth token management.
 * Matches implementation plan Component 8.
 */

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

// ── Token storage ──

let accessToken: string | null = null;

export function setAccessToken(token: string | null) {
  accessToken = token;
  if (token) {
    if (typeof window !== "undefined") localStorage.setItem("access_token", token);
  } else {
    if (typeof window !== "undefined") localStorage.removeItem("access_token");
  }
}

export function getAccessToken(): string | null {
  if (accessToken) return accessToken;
  if (typeof window !== "undefined") {
    accessToken = localStorage.getItem("access_token");
  }
  return accessToken;
}

let refreshToken: string | null = null;

export function setRefreshToken(token: string | null) {
  refreshToken = token;
  if (token) {
    if (typeof window !== "undefined") localStorage.setItem("refresh_token", token);
  } else {
    if (typeof window !== "undefined") localStorage.removeItem("refresh_token");
  }
}

export function getRefreshToken(): string | null {
  if (refreshToken) return refreshToken;
  if (typeof window !== "undefined") {
    refreshToken = localStorage.getItem("refresh_token");
  }
  return refreshToken;
}

// ── Core fetch wrapper ──

interface FetchOptions extends RequestInit {
  params?: Record<string, string | undefined>;
}

async function fetchAPI<T>(path: string, options: FetchOptions = {}): Promise<T> {
  const { params, ...fetchOpts } = options;

  // Build URL with query parameters
  let url = `${BACKEND_URL}${path}`;
  if (params) {
    const searchParams = new URLSearchParams();
    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined) searchParams.set(key, value);
    }
    const qs = searchParams.toString();
    if (qs) url += `?${qs}`;
  }

  // Add auth header
  const token = getAccessToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(fetchOpts.headers as Record<string, string> || {}),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    ...fetchOpts,
    headers,
  });

  if (response.status === 401) {
    // Try refresh
    const refreshed = await tryRefresh();
    if (refreshed) {
      headers["Authorization"] = `Bearer ${getAccessToken()}`;
      const retryResponse = await fetch(url, { ...fetchOpts, headers });
      if (!retryResponse.ok) {
        throw new APIError(retryResponse.status, await retryResponse.text());
      }
      return retryResponse.json();
    }
    // Redirect to login
    if (typeof window !== "undefined") {
      window.location.href = "/";
    }
    throw new APIError(401, "Unauthorized");
  }

  if (!response.ok) {
    const body = await response.text();
    throw new APIError(response.status, body);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}

async function uploadFile<T>(path: string, file: File): Promise<T> {
  const url = `${BACKEND_URL}${path}`;
  const token = getAccessToken();

  const formData = new FormData();
  formData.append("file", file);

  const headers: Record<string, string> = {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    method: "POST",
    headers,
    body: formData,
  });

  if (!response.ok) {
    const body = await response.text();
    throw new APIError(response.status, body);
  }

  return response.json();
}

async function tryRefresh(): Promise<boolean> {
  const rt = getRefreshToken();
  if (!rt) return false;

  try {
    const response = await fetch(`${BACKEND_URL}/api/v1/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: rt }),
    });

    if (!response.ok) return false;

    const data = await response.json();
    setAccessToken(data.access_token);
    setRefreshToken(data.refresh_token);
    return true;
  } catch {
    return false;
  }
}

// ── Error class ──

export class APIError extends Error {
  status: number;
  body: string;

  constructor(status: number, body: string) {
    super(`API Error ${status}: ${body}`);
    this.status = status;
    this.body = body;
  }
}

// ── Typed API client ──

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface UserProfile {
  name: string;
  headline: string;
  location: string;
  status: string;
  completionScore: number;
  skills: string[];
  experience: { id: string; role: string; company: string; period: string; bullets: string[] }[];
  education: { id: string; degree: string; institution: string; period: string }[];
}

export interface JobMatch {
  id: string;
  title: string;
  company: string;
  location: string;
  matchScore: number;
  salary?: string;
  postedAt: string;
  skills: string[];
  missingSkills: string[];
  reasons: string[];
}

export interface JobDetail extends JobMatch {
  description?: string;
  responsibilities: string[];
  experienceLevel?: string;
  jobType?: string;
  isRemote: boolean;
  isSaved: boolean;
}

export interface JobFeedResponse {
  jobs: JobMatch[];
  nextCursor: string | null;
  total: number;
}

export interface DashboardStats {
  totalParses: number;
  jobsMatched: number;
  interviewsSecured: number;
  profileAppearances: number;
  recentActivity: { id: string; action: string; time: string }[];
}

export interface ParsedResume {
  id: string;
  file_type: string;
  skills: string[];
  experience_years: number | null;
  keywords: string[];
  parsing_confidence: number | null;
  parsed_data: Record<string, unknown>;
}

export const api = {
  auth: {
    register: (email: string, password: string, name: string) =>
      fetchAPI<TokenResponse>("/api/v1/auth/register", {
        method: "POST",
        body: JSON.stringify({ email, password, name }),
      }),
    login: (email: string, password: string) =>
      fetchAPI<TokenResponse>("/api/v1/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      }),
    me: () => fetchAPI<{ id: string; email: string; name: string; role: string }>("/api/v1/auth/me"),
  },

  jobs: {
    getFeed: (cursor?: string) =>
      fetchAPI<JobFeedResponse>("/api/v1/jobs/feed", { params: { cursor } }),
    getDetail: (id: string) => fetchAPI<JobDetail>(`/api/v1/jobs/${id}`),
    search: (q: string) =>
      fetchAPI<{ jobs: JobMatch[]; total: number; query: string }>("/api/v1/jobs/search", {
        params: { q },
      }),
    save: (id: string) =>
      fetchAPI<{ success: boolean }>(`/api/v1/jobs/${id}/save`, { method: "POST" }),
    unsave: (id: string) =>
      fetchAPI<{ success: boolean }>(`/api/v1/jobs/${id}/save`, { method: "DELETE" }),
    apply: (id: string) =>
      fetchAPI<{ success: boolean }>(`/api/v1/jobs/${id}/apply`, { method: "POST" }),
    dismiss: (id: string) =>
      fetchAPI<{ success: boolean }>(`/api/v1/jobs/${id}/dismiss`, { method: "POST" }),
    getSaved: () => fetchAPI<{ jobs: JobMatch[] }>("/api/v1/jobs/saved"),
  },

  resume: {
    upload: (file: File) => uploadFile<{ id: string; file_url: string; file_type: string }>("/api/v1/resume/upload", file),
    get: () => fetchAPI<ParsedResume>("/api/v1/resume"),
    update: (data: { skills?: string[]; parsed_data?: Record<string, unknown> }) =>
      fetchAPI<ParsedResume>("/api/v1/resume", { method: "PUT", body: JSON.stringify(data) }),
    delete: () => fetchAPI<void>("/api/v1/resume", { method: "DELETE" }),
    getParsingStatus: () => {
      const token = getAccessToken();
      return new EventSource(
        `${BACKEND_URL}/api/v1/resume/parsing-status`,
        // Note: EventSource doesn't support custom headers natively.
        // For auth, the token would be passed as a query param or via cookie in production.
      );
    },
  },

  profile: {
    get: () => fetchAPI<UserProfile>("/api/v1/profile"),
    update: (data: Partial<UserProfile>) =>
      fetchAPI<UserProfile>("/api/v1/profile", { method: "PUT", body: JSON.stringify(data) }),
    updateSkills: (skills: string[]) =>
      fetchAPI<{ skills: string[] }>("/api/v1/profile/skills", {
        method: "PUT",
        body: JSON.stringify({ skills }),
      }),
    getSkillGaps: () =>
      fetchAPI<{ gaps: { skill: string; frequency: number; percentage: number }[]; total_jobs_analyzed: number }>(
        "/api/v1/profile/skill-gaps"
      ),
  },

  dashboard: {
    getStats: () => fetchAPI<DashboardStats>("/api/v1/dashboard/stats"),
    getApplications: () =>
      fetchAPI<{
        applications: { id: string; jobTitle: string; company: string; status: string; appliedAt: string }[];
        total: number;
      }>("/api/v1/dashboard/applications"),
    getMatchTrend: () =>
      fetchAPI<{ data: { week: string; avgScore: number }[] }>("/api/v1/dashboard/match-trend"),
  },
};
