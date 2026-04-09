"use client";

import React from "react";
import Link from "next/link";
import { Search, Bell, LogOut } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";

export interface TopNavBarProps {
  activeTab?: "jobs" | "dashboard" | "profile";
  onSearch?: () => void;
  searchQuery?: string;
  setSearchQuery?: (q: string) => void;
}

export const TopNavBar = ({ activeTab = "jobs", onSearch, searchQuery, setSearchQuery }: TopNavBarProps) => {
  const { user, isAuthenticated, logout } = useAuth();
  const initial = user?.name?.charAt(0) || isAuthenticated ? "U" : "?";

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-gray-200 bg-white/70 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-8">
          <Link href="/" className="text-xl font-bold text-primary tracking-tight">
            ResumeMatch AI
          </Link>

          <div className="relative hidden md:block w-72">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
              <Search className="h-4 w-4 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Search jobs, skills, companies..."
              value={searchQuery || ""}
              onChange={(e) => setSearchQuery?.(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && onSearch?.()}
              className="block w-full rounded-md border-0 py-1.5 pl-10 pr-3 text-gray-900 bg-gray-100 ring-1 ring-inset ring-transparent focus:ring-primary sm:text-sm sm:leading-6"
            />
          </div>
        </div>

        <div className="flex items-center gap-6">
          <div className="hidden sm:flex gap-4 text-sm font-medium text-gray-500">
            <Link href="/jobs" className={`hover:text-primary ${activeTab === 'jobs' ? 'text-primary border-b-2 border-primary h-16 flex items-center' : 'h-16 flex items-center'}`}>Jobs</Link>
            <Link href="/dashboard" className={`hover:text-primary ${activeTab === 'dashboard' ? 'text-primary border-b-2 border-primary h-16 flex items-center' : 'h-16 flex items-center'}`}>Dashboard</Link>
            <Link href="/profile" className={`hover:text-primary ${activeTab === 'profile' ? 'text-primary border-b-2 border-primary h-16 flex items-center' : 'h-16 flex items-center'}`}>Profile</Link>
          </div>

          <div className="flex items-center gap-4">
            <button className="text-gray-400 hover:text-gray-500">
              <Bell className="h-5 w-5" />
            </button>
            {isAuthenticated ? (
              <div className="flex items-center gap-2">
                <Link href="/profile" className="flex items-center gap-2">
                  <div className="h-8 w-8 rounded-full bg-gray-300 flex items-center justify-center overflow-hidden">
                    <span className="text-sm font-bold text-gray-600">{user?.name?.charAt(0) || "U"}</span>
                  </div>
                </Link>
                <button onClick={logout} className="text-gray-400 hover:text-red-500" title="Sign out">
                  <LogOut className="h-4 w-4" />
                </button>
              </div>
            ) : (
              <Link href="/" className="text-sm font-medium text-primary hover:underline">Sign In</Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};
