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

export const USER_PROFILE = {
  name: "Alex Sterling",
  headline: "Frontend Engineer specializing in React / UI UX",
  location: "San Francisco, CA",
  status: "Open to Work",
  completionScore: 85,
  skills: ["React", "TypeScript", "Next.js", "Tailwind CSS", "Figma"],
  experience: [
    {
      id: "exp1",
      role: "Senior Developer",
      company: "TechNova",
      period: "2021 - Present",
      bullets: [
        "Led migration to Next.js reducing load times by 40%.",
        "Managed a team of 4 frontend engineers.",
      ],
    },
  ],
  education: [
    {
      id: "edu1",
      degree: "B.S. Computer Science",
      institution: "State University",
      period: "2015 - 2019",
    },
  ],
};

export const JOB_MATCHES: JobMatch[] = [
  {
    id: "job1",
    title: "Senior Frontend Developer",
    company: "TechNova",
    location: "San Francisco, Hybrid",
    matchScore: 95,
    postedAt: "2 hours ago",
    skills: ["React", "TypeScript", "Next.js"],
    missingSkills: ["GraphQL"],
    reasons: [
      "4+ years React",
      "TypeScript experience",
      "Next.js architecture",
    ],
  },
  {
    id: "job2",
    title: "Frontend UI/UX Engineer",
    company: "DesignCo",
    location: "Remote",
    matchScore: 88,
    postedAt: "1 day ago",
    skills: ["React", "Tailwind CSS", "Figma"],
    missingSkills: ["Framer Motion", "Three.js"],
    reasons: ["Strong UI portfolio", "Tailwind mastery"],
  },
  {
    id: "job3",
    title: "Full Stack Developer (React Node)",
    company: "StartupInc",
    location: "New York, On-site",
    matchScore: 62,
    postedAt: "3 days ago",
    skills: ["React"],
    missingSkills: ["Node.js", "Express", "PostgreSQL"],
    reasons: ["Frontend mastery"],
  },
];

export const DASHBOARD_STATS = {
  totalParses: 24,
  jobsMatched: 1402,
  interviewsSecured: 3,
  profileAppearances: 45,
  recentActivity: [
    { id: "act1", action: "Matched with Google - 98%", time: "4 hrs ago" },
    { id: "act2", action: "Parsed new Resume v3", time: "2 hrs ago" },
    { id: "act3", action: "Profile viewed by TechNova", time: "1 day ago" },
  ],
};
