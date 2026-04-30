import { useEffect, useState } from "react";
import clsx from "clsx";
import type { TextToSignResult } from "../lib/api";

/**
 * Placeholder avatar — plays the gloss sequence as large animated cards.
 * The Android app swaps this for a rigged .glb + .bvh avatar; in the web
 * demo we keep the dependency surface tiny to make the build reproducible.
 */
export function AvatarPlayer({ result }: { result: TextToSignResult }) {
  const [clauseIdx, setClauseIdx] = useState(0);
  const [glossIdx, setGlossIdx] = useState(0);

  useEffect(() => {
    setClauseIdx(0);
    setGlossIdx(0);
  }, [result]);

  const clause = result.clauses[clauseIdx];
  const gloss = clause?.glosses[glossIdx];

  useEffect(() => {
    if (!clause) return;
    const perGloss = Math.max(450, clause.duration_ms / clause.glosses.length);
    const id = setTimeout(() => {
      if (glossIdx + 1 < clause.glosses.length) {
        setGlossIdx(glossIdx + 1);
      } else if (clauseIdx + 1 < result.clauses.length) {
        setClauseIdx(clauseIdx + 1);
        setGlossIdx(0);
      }
    }, perGloss);
    return () => clearTimeout(id);
  }, [clauseIdx, glossIdx, clause, result.clauses.length]);

  if (!clause) return null;

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 space-y-4">
      <div className="aspect-video bg-gradient-to-br from-slate-800 to-slate-950 rounded-xl flex flex-col items-center justify-center">
        <div
          key={`${clauseIdx}-${glossIdx}`}
          className="text-5xl font-black text-madad-gold animate-[pulse_0.8s_ease-in-out] text-center px-6"
        >
          {formatGloss(gloss)}
        </div>
        <div className="mt-3 text-xs text-slate-500 uppercase tracking-wider">
          Sign {glossIdx + 1} / {clause.glosses.length} · Clause {clauseIdx + 1}
          /{result.clauses.length}
        </div>
      </div>

      <div className="flex flex-wrap gap-1.5">
        {result.clauses.flatMap((c, ci) =>
          c.glosses.map((g, gi) => {
            const active = ci === clauseIdx && gi === glossIdx;
            return (
              <span
                key={`${ci}-${gi}`}
                className={clsx(
                  "px-2 py-1 rounded text-xs",
                  active
                    ? "bg-madad-gold text-madad-ink"
                    : "bg-slate-800 text-slate-400"
                )}
              >
                {g}
              </span>
            );
          })
        )}
      </div>

      {result.missing_vocab.length > 0 && (
        <p className="text-xs text-amber-300/80">
          Fingerspelled: {result.missing_vocab.join(", ")}
        </p>
      )}
      <p className="text-[11px] text-slate-500">
        {result.backend} · {result.latency_ms} ms
      </p>
    </div>
  );
}

function formatGloss(g: string | undefined): string {
  if (!g) return "";
  if (g.startsWith("Q:")) return `? ${g.slice(2)}`;
  if (g.startsWith("N:")) return `¬ ${g.slice(2)}`;
  if (g.startsWith("T:")) return `◆ ${g.slice(2)}`;
  if (g.startsWith("E:")) return `❗ ${g.slice(2)}`;
  if (g.startsWith("FS-")) return `✋ ${g.slice(3)}`;
  return g;
}
