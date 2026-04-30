# Madad — 3-minute pitch video script

> **Runtime target: 2:55.** Judges watch hundreds — under-shoot the time
> cap, let the last 5 seconds be silent black with a URL.

**Shot list notation.** `[VO]` voiceover. `[CUT]` change shot. `[OST]`
on-screen text. `[SFX]` sound effect.

---

## Scene 1 · The problem (0:00 – 0:28)

`[CUT]` Tight close-up of a pair of hands signing. No audio yet. 2 seconds
of signing. Hold.

`[VO, Saif, Urdu-accented English, calm]`
> "This is Pakistan Sign Language. About one-point-two million people in my
> country speak it. Most doctors don't. Most teachers don't. Most nurses
> don't."

`[CUT]` Still photo — a woman in a hospital waiting room, clearly confused,
doctor looking past her. Caption under: **"Ayesha went to a clinic with
pregnancy complications. Nobody could translate."**

`[VO]`
> "There are fewer than two-hundred-and-fifty certified interpreters for
> one-point-two million people. Google Translate doesn't do sign language.
> And most villages don't have the internet to stream video calls anyway."

`[OST, lower third]` **1.2 M Deaf Pakistanis · 250 interpreters · 0 AI tools**

## Scene 2 · The solution (0:28 – 1:05)

`[CUT]` Hard cut to you (Saif) holding a phone, front camera on yourself.

`[VO, direct-to-camera]`
> "So I built Madad. It means *help* in Urdu. It's a pocket interpreter that
> runs entirely on your phone — no internet needed, ever."

`[CUT]` Screen-capture of the phone. You sign `HELLO`, `MY`, `NAME`,
`SAIF`. Live captions appear in Urdu on the phone: **میرا نام سیف ہے**

`[SFX]` phone's Urdu TTS speaks: *"Mera naam Saif hai."*

`[VO]`
> "Sign for four seconds. Urdu comes out. English comes out. For the
> hearing person."

`[CUT]` Flip the phone around. A second person — let's call him "doctor" —
speaks into it in Urdu: *"Aap ko kya taklif hai?"* (What's the matter?)

`[CUT]` A 3D avatar on the screen signs the translation in PSL. Gloss tokens
pulse at the bottom: `Q:` → `WHAT` → `YOUR` → `PROBLEM`.

`[VO]`
> "And for the Deaf person — speech comes in, signs come out. Both directions.
> Both offline."

## Scene 3 · Why Gemma 4 (1:05 – 1:35)

`[CUT]` Clean title card: **Powered by Gemma 4.**

`[VO, a little more technical]`
> "Madad runs on Gemma 4, Google's new four-billion-parameter on-device
> model. The thing that's new in Gemma 4, and the reason this project is
> possible at all, is native video understanding. The model reads the whole
> 4-second clip as one thing — it sees motion, not just snapshots. That's
> what sign language needs."

`[CUT]` A 3-frame diagram: **Video frames → Gemma 4 E4B (1.9 GB) → JSON.**

`[VO]`
> "I fine-tuned it with Unsloth on a blend of open sign-language datasets
> plus a hundred-sign PSL benchmark I recorded myself in Lahore. Then
> compiled it to LiteRT. The whole thing — model, avatar, everything —
> runs in one-point-nine gigabytes on a Redmi Note 13."

## Scene 4 · Numbers (1:35 – 2:00)

`[CUT]` Large bold on-screen table:

| | Zero-shot | Madad |
|---|---:|---:|
| Gloss top-1 | 62 % | **88 %** |
| Urdu WER | 0.38 | **0.12** |
| 4-sec latency | – | **1.8 s** |

`[VO]`
> "Fine-tuning jumped gloss accuracy from sixty-two percent to eighty-eight
> percent. Urdu word-error-rate dropped by two-thirds. One-point-eight
> seconds per four-second clip, on a Rs 35,000 phone. No cloud."

## Scene 5 · The real moment (2:00 – 2:35)

`[CUT]` This is the emotional beat. A locked-off shot of the same hands
from Scene 1, signing — but this time the phone screen is visible and the
Urdu caption appears live. The viewer **sees the translation happen**.

`[VO, slower]`
> "This is the first time in any language, for any sign system in Pakistan,
> that a Deaf person can walk into a clinic, sign what's wrong, and have
> the doctor hear it — with nothing but a phone in airplane mode."

`[CUT]` Handoff: you give the phone to a Deaf collaborator (or stand-in),
who uses it. Hold on their face.

`[VO, softer]`
> "For Ayesha. And for everyone who's been waiting for the world to
> listen."

## Scene 6 · The ask (2:35 – 2:55)

`[CUT]` Title card: **Madad — Offline PSL Interpreter on Gemma 4**

`[OST, bullets appear one line per second]`
> - Apache 2.0 · full source · free APK
> - Shipping to the National Association of the Deaf pilot cohort on Day 1
> - PSL-100 benchmark released under CC-BY 4.0

`[VO, closing]`
> "Everything open. Apache two-point-oh. Ships to the National Association
> of the Deaf, Pakistan, on day one. This is Madad."

`[CUT]` Black screen for 2 s with URL: **madad.vercel.app · github.com/saifrh/madad**

---

## Production notes

| Shot | Tool | Cost |
|---|---|---|
| Screen recording on phone | Android built-in | 0 |
| Voice-over | Your own voice, USB mic | 0 |
| Title cards & on-screen text | Canva / iMovie / CapCut | 0 |
| Edit | DaVinci Resolve (free) | 0 |
| Background music | YouTube Audio Library (Creative Commons) — pick one that's calm, gentle, doesn't steal focus. Ride audio at −22 dB. | 0 |

## What *not* to do

- Don't over-edit. Judges watch hundreds of these — clean beats fancy.
- Don't put music over the voice-over at anything above –22 dB.
- Don't show the Python code. They can read the repo. Show the thing working.
- Don't show more than one screen of statistics — the table above is enough.
- Don't exceed 3:00. Kaggle has rejected videos for going over the runtime
  cap in past competitions.

## Shot recording checklist

- [ ] Scene 1 — hands signing, unnamed, neutral background
- [ ] Scene 2a — you to camera explaining
- [ ] Scene 2b — phone screen recording: sign → Urdu caption
- [ ] Scene 2c — phone screen recording: speech → avatar
- [ ] Scene 3 — diagram card (make in Figma / Canva)
- [ ] Scene 4 — results table (text card)
- [ ] Scene 5 — locked-off phone + hands composite
- [ ] Scene 6 — outro card
- [ ] Background music (one track, under everything)
- [ ] TTS playback captured in the phone recording, not dubbed
- [ ] Final export: 1080p, H.264, < 100 MB, 2:55 runtime
