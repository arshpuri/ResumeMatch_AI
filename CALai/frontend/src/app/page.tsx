"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { TopNavBar } from "@/components/shared/TopNavBar";
import { Button } from "@/components/shared/Button";
import { UploadCloud, FileText, CheckCircle2, LogIn } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { api, setAccessToken, setRefreshToken } from "@/lib/api";

export default function WelcomePage() {
  const { isAuthenticated, login, register } = useAuth();
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);
  const [showAuth, setShowAuth] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [authError, setAuthError] = useState("");

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!isAuthenticated) {
      setShowAuth(true);
      return;
    }

    setUploading(true);
    try {
      await api.resume.upload(file);
      router.push("/parsing");
    } catch (err) {
      alert(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setAuthError("");
    try {
      if (isLogin) {
        await login(email, password);
      } else {
        await register(email, password, name);
      }
      setShowAuth(false);
      // After auth, redirect to dashboard
      router.push("/dashboard");
    } catch (err: any) {
      setAuthError(err?.message || "Authentication failed");
    }
  };

  return (
    <div className="flex min-h-screen flex-col">
      <TopNavBar activeTab="jobs" />
      <main className="flex-grow bg-[#F3F2EF] px-4 py-12">
        <div className="mx-auto max-w-4xl space-y-8">

          <div className="text-center space-y-4">
            <h1 className="text-4xl font-extrabold tracking-tight text-primary">Discover Your Perfect Career Match</h1>
            <p className="text-lg text-text-muted">Upload your resume to instantly see which roles fit your skills best using our precise AI engine.</p>
          </div>

          {/* Auth Modal */}
          {showAuth && (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
              <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-2xl">
                <h2 className="text-2xl font-bold text-foreground mb-2">
                  {isLogin ? "Welcome back" : "Create account"}
                </h2>
                <p className="text-sm text-text-muted mb-6">
                  {isLogin ? "Sign in to continue" : "Get started with ResumeMatch AI"}
                </p>
                <form onSubmit={handleAuth} className="space-y-4">
                  {!isLogin && (
                    <input
                      type="text" placeholder="Full Name" value={name}
                      onChange={(e) => setName(e.target.value)} required
                      className="w-full rounded-lg border border-gray-200 px-4 py-3 text-sm focus:border-primary focus:ring-1 focus:ring-primary outline-none"
                    />
                  )}
                  <input
                    type="email" placeholder="Email" value={email}
                    onChange={(e) => setEmail(e.target.value)} required
                    className="w-full rounded-lg border border-gray-200 px-4 py-3 text-sm focus:border-primary focus:ring-1 focus:ring-primary outline-none"
                  />
                  <input
                    type="password" placeholder="Password" value={password}
                    onChange={(e) => setPassword(e.target.value)} required minLength={8}
                    className="w-full rounded-lg border border-gray-200 px-4 py-3 text-sm focus:border-primary focus:ring-1 focus:ring-primary outline-none"
                  />
                  {authError && <p className="text-sm text-red-500">{authError}</p>}
                  <Button type="submit" className="w-full">{isLogin ? "Sign In" : "Create Account"}</Button>
                </form>
                <p className="mt-4 text-center text-sm text-text-muted">
                  {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
                  <button onClick={() => setIsLogin(!isLogin)} className="font-semibold text-primary hover:underline">
                    {isLogin ? "Sign up" : "Sign in"}
                  </button>
                </p>
                <button onClick={() => setShowAuth(false)} className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 text-xl">&times;</button>
              </div>
            </div>
          )}

          <div className="mx-auto max-w-2xl">
            <div className="flex flex-col items-center justify-center rounded-2xl bg-surface p-12 text-center shadow-sm border border-dashed border-gray-300 transition-colors hover:border-primary/50">
              <UploadCloud className={`h-16 w-16 mb-6 ${uploading ? 'text-gray-400 animate-pulse' : 'text-primary'}`} />
              <h3 className="mb-2 text-xl font-semibold text-foreground">
                {uploading ? "Uploading..." : "Upload your Resume"}
              </h3>
              <p className="text-sm text-text-muted mb-8">PDF, DOCX, or TXT up to 10MB</p>

              <input ref={fileInputRef} type="file" accept=".pdf,.docx,.doc,.txt" className="hidden" onChange={handleFileSelect} />

              <div className="flex w-full flex-col gap-4 sm:w-auto sm:flex-row">
                <Button size="lg" className="w-full sm:w-48" onClick={() => {
                  if (!isAuthenticated) { setShowAuth(true); return; }
                  fileInputRef.current?.click();
                }} disabled={uploading}>
                  {uploading ? "Uploading..." : "Browse Files"}
                </Button>
                {!isAuthenticated && (
                  <>
                    <div className="flex items-center justify-center gap-2 text-sm text-gray-500">
                      <hr className="w-8 border-gray-200" /> or <hr className="w-8 border-gray-200" />
                    </div>
                    <Button variant="outline" size="lg" className="w-full sm:w-48 gap-2" onClick={() => setShowAuth(true)}>
                      <LogIn className="h-4 w-4" /> Sign In
                    </Button>
                  </>
                )}
              </div>
            </div>

            <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
               <div className="flex flex-col items-center gap-2 text-center">
                 <div className="flex h-12 w-12 items-center justify-center rounded-full bg-emerald-light text-emerald-solid"><FileText className="h-6 w-6" /></div>
                 <h4 className="font-semibold text-foreground">Deep Parsing</h4>
                 <p className="text-sm text-text-muted">We extract every crucial skill implicitly and explicitly.</p>
               </div>
               <div className="flex flex-col items-center gap-2 text-center">
                 <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-50 text-primary"><CheckCircle2 className="h-6 w-6" /></div>
                 <h4 className="font-semibold text-foreground">Verified Match</h4>
                 <p className="text-sm text-text-muted">AI correlates your skills strictly to job requisites.</p>
               </div>
               <div className="flex flex-col items-center gap-2 text-center">
                 <div className="flex h-12 w-12 items-center justify-center rounded-full bg-purple-50 text-purple-600"><UploadCloud className="h-6 w-6" /></div>
                 <h4 className="font-semibold text-foreground">One-Click Apply</h4>
                 <p className="text-sm text-text-muted">Bypass manual forms with your unified AI profile.</p>
               </div>
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}
