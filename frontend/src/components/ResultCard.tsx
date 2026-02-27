import { AlertTriangle, CheckCircle, ShieldAlert, ShieldCheck } from "lucide-react";
import type { DetectResult } from "@/lib/api";

interface ResultCardProps {
  result: DetectResult;
  index?: number;
}

export function ResultCard({ result, index }: ResultCardProps) {
  const isFake = result.is_fake;
  const pct = (result.confidence * 100).toFixed(1);

  return (
    <div
      className={`animate-scale-in rounded-xl border-2 p-6 transition-all card-elevated ${
        isFake ? "result-fake" : "result-real"
      }`}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-center gap-4">
          <div
            className={`flex h-12 w-12 items-center justify-center rounded-xl ${
              isFake ? "bg-destructive/15" : "bg-success/15"
            }`}
          >
            {isFake ? (
              <ShieldAlert className="h-6 w-6" />
            ) : (
              <ShieldCheck className="h-6 w-6" />
            )}
          </div>
          <div>
            {index !== undefined && (
              <p className="mb-0.5 text-[11px] font-semibold uppercase tracking-widest opacity-50">
                Article #{index + 1}
              </p>
            )}
            <h3 className="font-display text-2xl font-bold leading-tight">
              {isFake ? "Likely Fake" : "Likely Real"}
            </h3>
          </div>
        </div>
        <div
          className={`shrink-0 rounded-lg px-3.5 py-2 text-center ${
            isFake ? "bg-destructive/10" : "bg-success/10"
          }`}
        >
          <p className="font-display text-xl font-bold leading-none">{pct}%</p>
          <p className="mt-0.5 text-[10px] font-medium uppercase tracking-wider opacity-60">
            confidence
          </p>
        </div>
      </div>

      {/* Confidence bar */}
      <div className="mt-5 h-2 w-full overflow-hidden rounded-full bg-card/80">
        <div
          className={`h-full rounded-full animate-bar-fill ${
            isFake ? "bg-destructive" : "bg-success"
          }`}
          style={{ "--bar-width": `${pct}%` } as React.CSSProperties}
        />
      </div>

      {result.text && (
        <p className="mt-4 line-clamp-2 rounded-lg bg-card/50 p-3 text-sm italic opacity-70">
          "{result.text.slice(0, 140)}…"
        </p>
      )}

      <p className="mt-4 text-sm leading-relaxed opacity-75">
        {isFake
          ? "This article shows linguistic patterns commonly associated with misinformation. We recommend verifying claims with multiple trusted sources before sharing."
          : "This article's structure and language patterns are consistent with credible reporting. As always, cross-reference important claims with other sources."}
      </p>
    </div>
  );
}
