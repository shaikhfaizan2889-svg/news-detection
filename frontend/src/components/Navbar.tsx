import { Sun, Moon, Shield } from "lucide-react";
import { useTheme } from "@/hooks/useTheme";
import { HealthIndicator } from "./HealthIndicator";

export function Navbar() {
  const { dark, toggle } = useTheme();

  return (
    <header className="nav-glass sticky top-0 z-50 border-b">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-2.5 story-link">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-destructive/10">
            <Shield className="h-5 w-5 text-destructive" />
          </div>
          <span className="font-display text-xl font-bold tracking-tight">
            VerityCheck
          </span>
        </div>

        <div className="flex items-center gap-3">
          <HealthIndicator />
          <div className="h-5 w-px bg-border" />
          <button
            onClick={toggle}
            className="flex h-9 w-9 items-center justify-center rounded-lg text-muted-foreground transition-all duration-200 hover:bg-accent hover:text-accent-foreground hover:scale-105 active:scale-95"
            aria-label="Toggle theme"
          >
            {dark ? <Sun className="h-[18px] w-[18px]" /> : <Moon className="h-[18px] w-[18px]" />}
          </button>
        </div>
      </div>
    </header>
  );
}
