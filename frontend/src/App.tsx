import { useState } from "react";
import clsx from "clsx";
import { Hand, Mic2 } from "lucide-react";
import { SignCamera } from "./components/SignCamera";
import { VoiceToSign } from "./components/VoiceToSign";
import { HealthBadge } from "./components/HealthBadge";

type Mode = "sign" | "voice";

export default function App() {
  const [mode, setMode] = useState<Mode>("sign");

  return (
    <div className="min-h-full flex flex-col">
      <header className="px-6 pt-6 pb-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Logo />
          <div>
            <h1 className="text-xl font-bold tracking-tight">
              Madad <span className="text-slate-500 font-normal">مدد</span>
            </h1>
            <p className="text-xs text-slate-400">
              Offline Pakistan Sign Language interpreter · Gemma 4
            </p>
          </div>
        </div>
        <HealthBadge />
      </header>

      <div className="px-6 pb-3">
        <div className="inline-flex bg-slate-900/60 border border-slate-800 rounded-full p-1">
          <ModeButton
            active={mode === "sign"}
            onClick={() => setMode("sign")}
            icon={<Hand size={16} />}
            label="Sign → Speech"
          />
          <ModeButton
            active={mode === "voice"}
            onClick={() => setMode("voice")}
            icon={<Mic2 size={16} />}
            label="Voice → Sign"
          />
        </div>
      </div>

      <main className="flex-1 px-6 pb-10">
        <div className="max-w-xl mx-auto">
          {mode === "sign" ? <SignCamera /> : <VoiceToSign />}
        </div>
      </main>

      <footer className="px-6 py-4 border-t border-slate-900 text-xs text-slate-500 flex justify-between">
        <span>
          Submission to the{" "}
          <a
            className="underline hover:text-madad-gold"
            href="https://www.kaggle.com/competitions/gemma-4-good-hackathon"
          >
            Gemma 4 Good Hackathon
          </a>
        </span>
        <span>Lahore, Pakistan</span>
      </footer>
    </div>
  );
}

function ModeButton({
  active,
  onClick,
  icon,
  label,
}: {
  active: boolean;
  onClick: () => void;
  icon: React.ReactNode;
  label: string;
}) {
  return (
    <button
      onClick={onClick}
      className={clsx(
        "flex items-center gap-2 px-4 py-1.5 rounded-full text-sm transition",
        active
          ? "bg-madad-gold text-madad-ink font-semibold"
          : "text-slate-400 hover:text-slate-200"
      )}
    >
      {icon}
      {label}
    </button>
  );
}

function Logo() {
  return (
    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-madad-gold to-amber-600 grid place-items-center">
      <Hand className="text-madad-ink" size={22} />
    </div>
  );
}
