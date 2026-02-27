import { useQuery } from "@tanstack/react-query";
import { fetchHealth } from "@/lib/api";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

export function HealthIndicator() {
  const { data, isError, isLoading } = useQuery({
    queryKey: ["health"],
    queryFn: fetchHealth,
    refetchInterval: 30_000,
    retry: 1,
  });

  const online = data?.status === "healthy" && data.model_loaded;

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <span
            className={`inline-block h-2.5 w-2.5 rounded-full ${
              isLoading
                ? "animate-pulse-dot bg-warning"
                : isError
                ? "bg-destructive"
                : online
                ? "bg-success"
                : "bg-destructive"
            }`}
          />
          <span className="hidden sm:inline">
            {isLoading ? "Connecting…" : isError ? "Offline" : online ? "Model ready" : "Degraded"}
          </span>
        </div>
      </TooltipTrigger>
      <TooltipContent side="bottom">
        {data ? (
          <div className="space-y-1 text-xs">
            <p>Model: {data.model_name}</p>
            <p>Accuracy: {(data.model_accuracy * 100).toFixed(1)}%</p>
            <p>Status: {data.status}</p>
          </div>
        ) : (
          <p className="text-xs">{isError ? "Cannot reach API" : "Checking…"}</p>
        )}
      </TooltipContent>
    </Tooltip>
  );
}
