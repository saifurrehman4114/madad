import { useCallback, useEffect, useRef, useState } from "react";

interface Options {
  maxSeconds?: number;
  mimeType?: string;
}

export function useRecorder(options: Options = {}) {
  const maxSeconds = options.maxSeconds ?? 4;
  const mimeType = options.mimeType ?? "video/webm;codecs=vp9,opus";

  const videoRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const [ready, setReady] = useState(false);
  const [recording, setRecording] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const attach = useCallback(async (el: HTMLVideoElement | null) => {
    videoRef.current = el;
    if (!el) return;
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: "user" },
        audio: true,
      });
      streamRef.current = stream;
      el.srcObject = stream;
      await el.play().catch(() => {});
      setReady(true);
    } catch (e) {
      setError((e as Error).message);
    }
  }, []);

  const record = useCallback(
    () =>
      new Promise<Blob>((resolve, reject) => {
        if (!streamRef.current) {
          reject(new Error("camera not ready"));
          return;
        }
        chunksRef.current = [];
        const rec = new MediaRecorder(streamRef.current, { mimeType });
        recorderRef.current = rec;
        rec.ondataavailable = (e) => e.data.size && chunksRef.current.push(e.data);
        rec.onstop = () =>
          resolve(new Blob(chunksRef.current, { type: mimeType }));
        rec.onerror = (e) => reject(new Error(String(e)));
        rec.start();
        setRecording(true);
        setTimeout(() => {
          rec.state !== "inactive" && rec.stop();
          setRecording(false);
        }, maxSeconds * 1000);
      }),
    [mimeType, maxSeconds]
  );

  useEffect(
    () => () => {
      streamRef.current?.getTracks().forEach((t) => t.stop());
    },
    []
  );

  return { attach, record, ready, recording, error };
}
