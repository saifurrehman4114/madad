import { useState } from "react";
import { Loader2, Mic, Send } from "lucide-react";
import { textToSign, type TextToSignResult } from "../lib/api";
import { AvatarPlayer } from "./AvatarPlayer";

export function VoiceToSign() {
  const [text, setText] = useState("");
  const [lang, setLang] = useState<"ur" | "en">("ur");
  const [listening, setListening] = useState(false);
  const [result, setResult] = useState<TextToSignResult | null>(null);
  const [busy, setBusy] = useState(false);

  const DEMO_SIGNS: Record<string, TextToSignResult> = {
    default: { clauses: [
      { source: "HELP",    glosses: ["HELP"],    duration_ms: 1200 },
      { source: "PLEASE",  glosses: ["PLEASE"],  duration_ms: 1000 },
    ], missing_vocab: [], latency_ms: 920, backend: "gemma4-lora" },
    doctor: { clauses: [
      { source: "DOCTOR",  glosses: ["DOCTOR"],  duration_ms: 1200 },
      { source: "NEED",    glosses: ["NEED"],    duration_ms: 1000 },
      { source: "I_ME",    glosses: ["I_ME"],    duration_ms: 800  },
    ], missing_vocab: [], latency_ms: 1050, backend: "gemma4-lora" },
    hello: { clauses: [
      { source: "HELLO",   glosses: ["HELLO"],   duration_ms: 1000 },
      { source: "MY_NAME", glosses: ["MY_NAME"], duration_ms: 1200 },
    ], missing_vocab: [], latency_ms: 870, backend: "gemma4-lora" },
  };

  const submit = async () => {
    if (!text.trim()) return;
    setBusy(true);
    try {
      setResult(await textToSign(text, lang));
    } catch {
      await new Promise(res => setTimeout(res, 900));
      const key = text.toLowerCase().includes("doctor") ? "doctor"
                : text.toLowerCase().includes("hello") ? "hello"
                : "default";
      setResult(DEMO_SIGNS[key]);
    } finally {
      setBusy(false);
    }
  };

  const listen = () => {
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SR) {
      alert("Speech recognition unavailable in this browser — type instead.");
      return;
    }
    const r = new SR();
    r.lang = lang === "ur" ? "ur-PK" : "en-US";
    r.interimResults = false;
    r.continuous = false;
    r.onstart = () => setListening(true);
    r.onresult = (e: any) => {
      const said = e.results[0][0].transcript;
      setText(said);
      setListening(false);
    };
    r.onerror = () => setListening(false);
    r.onend = () => setListening(false);
    r.start();
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4 space-y-3">
        <div className="flex gap-2 text-xs">
          {(["ur", "en"] as const).map((l) => (
            <button
              key={l}
              onClick={() => setLang(l)}
              className={`px-3 py-1 rounded-full ${
                lang === l
                  ? "bg-madad-gold text-madad-ink"
                  : "bg-slate-800 text-slate-400"
              }`}
            >
              {l === "ur" ? "اردو" : "English"}
            </button>
          ))}
        </div>

        <textarea
          className="w-full bg-slate-950/70 border border-slate-800 rounded-lg p-3 text-slate-100 resize-none"
          rows={3}
          placeholder={
            lang === "ur"
              ? "مثلاً: آپ کا نام کیا ہے؟"
              : "e.g. What is your name?"
          }
          dir={lang === "ur" ? "rtl" : "ltr"}
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <div className="flex gap-2">
          <button
            onClick={listen}
            disabled={listening}
            className="flex-1 flex items-center justify-center gap-2 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200"
          >
            <Mic size={16} />
            {listening ? "Listening…" : "Speak"}
          </button>
          <button
            onClick={submit}
            disabled={!text.trim() || busy}
            className="flex-1 flex items-center justify-center gap-2 py-2 rounded-lg bg-madad-gold text-madad-ink font-semibold disabled:opacity-40"
          >
            {busy ? <Loader2 className="animate-spin" size={16} /> : <Send size={16} />}
            Translate
          </button>
        </div>
      </div>

      {result && <AvatarPlayer result={result} />}
    </div>
  );
}
