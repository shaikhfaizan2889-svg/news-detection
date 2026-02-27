import { Shield, Github } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t bg-card py-10">
      <div className="container">
        <div className="flex flex-col items-center gap-6 sm:flex-row sm:justify-between">
          <div className="flex items-center gap-2 text-muted-foreground">
            <div className="flex h-7 w-7 items-center justify-center rounded-md bg-destructive/10">
              <Shield className="h-4 w-4 text-destructive" />
            </div>
            <span className="font-display text-sm font-semibold">VerityCheck</span>
          </div>

          <p className="max-w-sm text-center text-xs leading-relaxed text-muted-foreground sm:text-right">
            AI-powered analysis. Results are probabilistic and should not be the
            sole basis for judgment. Always verify with trusted sources.
          </p>
        </div>

        <div className="mt-6 flex items-center justify-center gap-6 border-t pt-6">
          <span className="text-xs text-muted-foreground/60">
            © {new Date().getFullYear()} VerityCheck
          </span>
        </div>
      </div>
    </footer>
  );
}
