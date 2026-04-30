import { useEffect, useState } from "react";
import { ShieldCheck, ShieldAlert } from "lucide-react";
import { health, type HealthReport } from "../lib/api";

export function HealthBadge() {
  const [h, setH] = useState<HealthReport | null>(null);

  useEffect(() => {
    let cancelled = false;
    const poll = async () => {
      try {
        const r = await health();
        if (!cancelled) setH(r);
      } catch {
        if (!cancelled)
          setH({ status: "offline", backend: "none", model: "none" });
      }
    };
    poll();
    const id = setInterval(poll, 10_000);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, []);

  const ok = h?.status === "ok";
  return (
    <div
      className={`inline-flex items-center gap-2 text-xs px-3 py-1.5 rounded-full border ${
        ok
          ? "border-emerald-500/40 text-emerald-300 bg-emerald-500/10"
          : "border-rose-500/40 text-rose-300 bg-rose-500/10"
      }`}
    >
      {ok ? <ShieldCheck size={14} /> : <ShieldAlert size={14} />}
      <span className="font-mono">
        {h?.backend ?? "…"} · {h?.model ?? "—"}
        {h?.adapter ? ` · ${h.adapter}` : ""}
      </span>
    </div>
  );
}
