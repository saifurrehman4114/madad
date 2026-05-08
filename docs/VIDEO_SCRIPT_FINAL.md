# Madad — Final Video Script
# Read this aloud. Total runtime: ~2 min 45 sec.
# [DIRECTIONS] tell you what to show on screen at that moment.
# Speak naturally — don't rush. One breath between each paragraph.

---

## OPENING — face on camera, 20 seconds

"In Pakistan, there are one point two million deaf people —
and only two hundred and fifty sign language interpreters.

That means if you're deaf, and you need to see a doctor,
or talk to a teacher, or call for help in an emergency —
there's almost no one there for you.

This is Madad. Madad means 'help' in Urdu. And that's exactly what it does."

---

## SWITCH TO SCREEN — open Chrome at localhost:5173

[SHOW: the Madad web app homepage — the full UI with the mode toggle at the top]

"Madad is a Pakistan Sign Language interpreter that runs completely offline —
no internet, no cloud, no account required — on any modern Android phone.

You can see it here running in the browser.
There are two modes — Sign to Speech, and Voice to Sign."

---

[CLICK: the "Sign → Speech" tab — show the camera view / upload area]

"In Sign to Speech mode, the app watches the user sign through the camera.
It samples four frames per second, sends them to Gemma 4 running on the device,
and returns the translation — in Urdu, in English, and as a gloss sequence —
in about one second."

[POINT to the urdu text display area on screen]

"The Urdu caption appears here in Nastaliq script — the natural script for Urdu —
so a hearing person standing next to a deaf user can read it instantly."

---

[CLICK: the "Voice → Sign" tab]

"In Voice to Sign mode, a hearing person speaks or types in Urdu or English —
and Madad converts it to a Pakistan Sign Language gloss sequence
for an animated avatar to perform."

[POINT to the avatar / gloss card section]

"The avatar plays each sign in sequence, with the correct timing and
non-manual markers — things like raised eyebrows for a question,
or a head shake for negation — that are part of PSL grammar."

---

## TECHNICAL — stay on screen, scroll or switch tab

[SHOW: the Kaggle notebook page — kaggle.com/code/saifurrehman4114ucp/madad-psl-interpreter]

"Under the hood, Madad runs Gemma 4 E4B — Google DeepMind's four-billion parameter
multimodal model — fine-tuned on PSL-100, the first publicly-licensed Pakistan Sign
Language benchmark I created for this project.

The fine-tuning was done with Unsloth LoRA on a Kaggle T4 GPU.
You can see the full training notebook here — it runs end to end in under thirty minutes."

[SCROLL the notebook briefly to show training output / benchmark results]

"After fine-tuning, the model is exported to LiteRT int4 format —
two point four gigabytes — and runs in real time on a Pixel 8 with no internet at all."

---

## IMPACT — back to the app or GitHub

[SHOW: github.com/saifurrehman4114/madad]

"Everything here is open source — Apache 2.0.
The PSL-100 benchmark is CC-BY 4.0 — free for researchers and NGOs to build on.
The adapter weights are public domain.

I've already reached out to Deaf Reach — a school for deaf students in Pakistan —
and the National Association of the Deaf, to pilot this with real students
and get the benchmark reviewed by certified PSL signers."

---

## CLOSE — face back on camera, 15 seconds

"Madad doesn't need a data plan. It doesn't need a subscription.
It doesn't need an interpreter to be available.

It just needs to be on your phone.

I built this for Ayesha — a fourteen-year-old deaf student in Lahore —
who should be able to visit a doctor on her own.

Thank you."

---

# PRODUCTION NOTES
# - Record the two "face on camera" sections on your phone (landscape, face a window).
# - Record the screen sections with Loom or OBS while Chrome is open.
# - Edit in CapCut: face clip → screen recording → face clip.
# - Total: under 3 minutes.
# - Upload unlisted to YouTube, paste the link in the Kaggle Discussion tab.
