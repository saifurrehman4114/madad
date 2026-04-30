# Cover image spec

Kaggle displays a 1200 × 630 cover image on every writeup. This is the
first thing a judge scrolling the list sees. Nail it.

## Concept

**Hero composition:** A pair of signing hands fills the left 40 % of the
frame. On the right, a phone screen shows the live Urdu caption in
Nastaliq. The two meet in the middle.

## Spec

| Element | Value |
|---|---|
| Dimensions | 1200 × 630 px |
| Format | PNG (lossless, no JPEG artefacts on text) |
| Text | "Madad · مدد" top-left, 72 pt, weight 800. Subtitle "Offline PSL interpreter · Gemma 4" 28 pt, weight 500 |
| Brand gold | `#F5B700` |
| Ink | `#0B0F1A` |
| Pine (accents) | `#054A29` |
| Typography | Inter (Latin) · Noto Nastaliq Urdu (Urdu) |
| Photo | Signing hands — bright neutral background, no face visible. Warm light. |
| Phone mockup | Pixel 8 front face, showing the Urdu caption `میرا نام سیف ہے` in yellow on dark. |
| Logo | Top-right, the hand-in-gold-square mark (see `assets/logo.svg`). |

## Generation

I don't have a Photoshop licence. The fastest zero-cost route:

1. Open **Figma** (free) → new 1200 × 630 frame.
2. Stock hand photo: Pexels or Unsplash, search "sign language hands"
   filtered to free-commercial-use. Two strong candidates:
   - [Pexels · SHVETS / ID 7516363](https://www.pexels.com/photo/7516363/)
   - [Pexels · Kindel Media / ID 8172318](https://www.pexels.com/photo/8172318/)
3. Phone mockup: Figma community has free Pixel 8 mockup frames — search
   "Pixel 8 mockup". Paste a 1080 × 2400 screenshot of Madad showing the
   caption into the mockup.
4. Text layer with the title + subtitle.
5. Export as PNG.

Target: 15 minutes of design time. If you want, I can write the exact
Figma node tree for a plugin to generate it deterministically — tell me.

## Alt: AI-generated hero image (Gemini or Imagen)

If you'd rather not shoot / source a photo, prompt for Gemini Imagen:

> "Cinematic close-up of two warm-toned hands mid-sign against a soft
> neutral gradient background. Left side of frame. Empty space on the
> right. Golden hour lighting. 16:9. No faces, no text, no watermarks."

Then composite the phone mockup + text on top in Figma.

## Logo (tiny SVG)

Already generated at `assets/logo.svg`. It's the gold hand-in-rounded-
square that the app bar uses.
