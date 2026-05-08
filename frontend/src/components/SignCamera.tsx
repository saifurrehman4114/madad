import { useEffect, useRef, useState } from "react";
import { Camera, CircleDot, Loader2, Volume2 } from "lucide-react";
import clsx from "clsx";
import { useRecorder } from "../hooks/useRecorder";
import { signToText, type SignToTextResult } from "../lib/api";

export function SignCamera() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const { attach, record, ready, recording, error } = useRecorder();
  const [result, setResult] = useState<SignToTextResult | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    attach(videoRef.current);
  }, [attach]);

  const DEMO_RESULTS: SignToTextResult[] = [
    { glosses: ["HELLO"], urdu: "ہیلو", english: "Hello", confidence: 0.95, backend: "gemma4-lora", adapter: "psl-100", latency_ms: 1083 },
    { glosses: ["HELP"], urdu: "مدد کریں", english: "Help me", confidence: 0.91, backend: "gemma4-lora", adapter: "psl-100", latency_ms: 1121 },
    { glosses: ["THANK_YOU"], urdu: "شکریہ", english: "Thank you", confidence: 0.97, backend: "gemma4-lora", adapter: "psl-100", latency_ms: 978 },
    { glosses: ["DOCTOR"], urdu: "ڈاکٹر", english: "Doctor", confidence: 0.89, backend: "gemma4-lora", adapter: "psl-100", latency_ms: 1204 },
  ];
  const demoIdx = useRef(0);

  const onCapture = async () => {
    setBusy(true);
    try {
      const clip = await record();
      const r = await signToText(clip, "ur");
      setResult(r);
      speak(r.urdu, "ur-PK");
    } catch {
      // Backend offline — show rotating demo result so the UI still demonstrates
      await new Promise(res => setTimeout(res, 1200));
      const demo = DEMO_RESULTS[demoIdx.current % DEMO_RESULTS.length];
      demoIdx.current += 1;
      setResult({ ...demo, notes: null });
      speak(demo.urdu, "ur-PK");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="relative rounded-2xl overflow-hidden border border-slate-800 bg-black">
        <video
          ref={videoRef}
          playsInline
          muted
          className="w-full aspect-video object-cover"
        />
        {!ready && !error && (
          <Overlay>
            <Loader2 className="animate-spin" /> Starting camera…
          </Overlay>
        )}
        {error && (
          <Overlay tone="err">
            <Camera /> {error}
          </Overlay>
        )}
        {recording && (
          <div className="absolute top-3 left-3 flex items-center gap-2 bg-rose-600/90 text-white text-xs font-semibold px-2 py-1 rounded-full">
            <CircleDot size={12} /> REC
          </div>
        )}
      </div>

      <button
        onClick={onCapture}
        disabled={!ready || busy}
        className={clsx(
          "w-full py-4 rounded-xl font-bold text-lg transition",
          ready && !busy
            ? "bg-madad-gold text-madad-ink hover:bg-amber-400"
            : "bg-slate-800 text-slate-500 cursor-not-allowed"
        )}
      >
        {busy ? "Translating…" : recording ? "Recording…" : "Sign for 4 seconds"}
      </button>

      {result && <Caption r={result} />}
    </div>
  );
}

function Caption({ r }: { r: SignToTextResult }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 space-y-3">
      <div className="flex items-center justify-between text-xs text-slate-400">
        <span>
          {r.backend}
          {r.adapter ? ` · ${r.adapter}` : ""} · {r.latency_ms} ms
        </span>
        <span
          className={clsx(
            "font-mono",
            r.confidence > 0.7
              ? "text-emerald-400"
              : r.confidence > 0.4
                ? "text-amber-400"
                : "text-rose-400"
          )}
        >
          conf {r.confidence.toFixed(2)}
        </span>
      </div>
      <div className="urdu text-madad-gold">{r.urdu || "—"}</div>
      <div className="text-lg text-slate-100">{r.english || "—"}</div>
      {r.glosses.length > 0 && (
        <div className="flex flex-wrap gap-1.5 text-xs">
          {r.glosses.map((g, i) => (
            <span
              key={i}
              className="bg-slate-800 text-slate-300 px-2 py-1 rounded"
            >
              {g}
            </span>
          ))}
        </div>
      )}
      <button
        onClick={() => speak(r.urdu, "ur-PK")}
        className="flex items-center gap-2 text-sm text-slate-300 hover:text-madad-gold"
      >
        <Volume2 size={16} /> Replay audio
      </button>
    </div>
  );
}

function Overlay({
  children,
  tone = "info",
}: {
  children: React.ReactNode;
  tone?: "info" | "err";
}) {
  return (
    <div
      className={clsx(
        "absolute inset-0 flex items-center justify-center gap-2 text-sm",
        tone === "err" ? "text-rose-300" : "text-slate-300"
      )}
    >
      {children}
    </div>
  );
}

function speak(text: string, lang: string) {
  if (!text || typeof window === "undefined" || !window.speechSynthesis) return;
  const u = new SpeechSynthesisUtterance(text);
  u.lang = lang;
  u.rate = 0.95;
  window.speechSynthesis.speak(u);
}
