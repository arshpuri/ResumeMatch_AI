import { TopNavBar } from "@/components/shared/TopNavBar";
import { Loader2, CheckCircle } from "lucide-react";

export default function ParsingLoadingPage() {
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
              <div className="flex items-center gap-4 text-emerald-solid">
                <CheckCircle className="h-6 w-6" />
                <span className="font-medium">File accepted and decrypted</span>
              </div>
              <div className="flex items-center gap-4 text-emerald-solid">
                <CheckCircle className="h-6 w-6" />
                <span className="font-medium">Information density scanned</span>
              </div>
              <div className="flex items-center gap-4 text-primary">
                <Loader2 className="h-6 w-6 animate-spin" />
                <span className="font-medium animate-pulse">Mapping NLP skill ontology...</span>
              </div>
              <div className="flex items-center gap-4 text-gray-400">
                <div className="h-6 w-6 rounded-full border-2 border-gray-200"></div>
                <span className="font-medium">Building custom knowledge graph</span>
              </div>
            </div>
            
            <div className="mt-10 mb-2 h-2 w-full overflow-hidden rounded-full bg-gray-100">
              <div className="h-full bg-gradient-to-r from-primary to-[var(--color-primary-container)] rounded-full w-2/3 animate-pulse"></div>
            </div>
            <p className="text-xs text-right text-text-muted">66% Complete</p>
          </div>
          
        </div>
      </main>
    </div>
  );
}
