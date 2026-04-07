import { TopNavBar } from "@/components/shared/TopNavBar";
import { Button } from "@/components/shared/Button";
import { UploadCloud, FileText, CheckCircle2 } from "lucide-react";

export default function WelcomePage() {
  return (
    <div className="flex min-h-screen flex-col">
      <TopNavBar activeTab="jobs" />
      <main className="flex-grow bg-[#F3F2EF] px-4 py-12">
        <div className="mx-auto max-w-4xl space-y-8">
          
          <div className="text-center space-y-4">
            <h1 className="text-4xl font-extrabold tracking-tight text-primary">Discover Your Perfect Career Match</h1>
            <p className="text-lg text-text-muted">Upload your resume to instantly see which roles fit your skills best using our precise AI engine.</p>
          </div>

          <div className="mx-auto max-w-2xl">
            <div className="flex flex-col items-center justify-center rounded-2xl bg-surface p-12 text-center shadow-sm border border-dashed border-gray-300 transition-colors hover:border-primary/50">
              <UploadCloud className="h-16 w-16 text-primary mb-6" />
              <h3 className="mb-2 text-xl font-semibold text-foreground">Upload your Resume</h3>
              <p className="text-sm text-text-muted mb-8">PDF, DOCX, or TXT up to 10MB</p>
              
              <div className="flex w-full flex-col gap-4 sm:w-auto sm:flex-row">
                <Button size="lg" className="w-full sm:w-48">Browse Files</Button>
                <div className="flex items-center justify-center gap-2 text-sm text-gray-500">
                  <hr className="w-8 border-gray-200" /> or <hr className="w-8 border-gray-200" />
                </div>
                <Button variant="outline" size="lg" className="w-full sm:w-48">Import from LinkedIn</Button>
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
