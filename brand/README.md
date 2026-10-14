# IvoryCoast Advisory brand kit

Quick reference for the logo, color and type. The full guidelines (clear space,
misuse, stationery, digital, presentation) live in the design canvas:
https://claude.ai/artifact/JrEWNKBPgTEm8eyL4AagJs

```
brand/
  logo/svg/     source artwork, all text outlined (no fonts needed)
  logo/png/     transparent PNG exports
  tokens/       brand.css (CSS custom properties) and brand.json
```

## The name

Write it **IvoryCoast Advisory**: one word, capital C, no space. The legal name
is **IvoryCoast Advisory LLC**; use it in contracts and footers. The domain is
always lowercase: `ivorycoastadvisory.com`. Not "Ivory Coast Advisory",
"Ivorycoast", "IVORYCOAST" or "ICA" in client-facing copy.

## Logo files

| Use | File |
| --- | --- |
| Default, light grounds | `logo/svg/lockup-horizontal.svg` |
| Narrow or square formats | `logo/svg/lockup-stacked.svg` |
| Small spaces (no descriptor) | `logo/svg/lockup-compact.svg`; `lockup-compact-small.svg` (heavier line) for 200 to 300 px wide, e.g. the site nav |
| Dark grounds | `logo/svg/lockup-horizontal-reversed.svg` (also `-compact`, `-stacked`) |
| Single-ink print | `...-navy.svg` |
| Reversed single ink | `...-white.svg` |
| Foil, emboss | `...-gold.svg` |
| Crest alone | `logo/svg/mark.svg`; `mark-small.svg` below 48 px |
| App icon, favicon | `logo/svg/icon-app.svg`, `icon-favicon.svg` (PNG 16/32/48/64/180/192/512) |
| Social avatars | `logo/svg/avatar-light.svg`, `avatar-dark.svg` |

Every variant exists as `color`, `reversed`, `navy`, `white` and `gold`
(unsuffixed files are the full-color version).

**Clear space.** Keep X clear on all sides, where X is the cap height of the
"I" in IvoryCoast. For the crest on its own, X is a quarter of its width.

**Minimum widths (screen).** Horizontal lockup 360 px, compact 200 px, stacked
280 px, crest 48 px (`mark-small` down to 24 px), favicon 16 px.

**Never** stretch, rotate, recolor, add effects, set on mid-tones or busy
imagery, retype the name, crop, or rearrange the lockup.

## Color

| Name | Hex | Role |
| --- | --- | --- |
| Ink Navy | `#172033` | Text, dark grounds, wordmark |
| Heritage Gold | `#A9791C` | Accents, rules, buttons, large type |
| Ivory | `#F6F1E4` | The page |
| Emerald | `#1F5B4C` | Labels, eyebrows |
| Slate | `#4B5468` | Body text |
| Antique Gold | `#9C7519` | "Advisory" in the logo, numerals |
| Bronze Text | `#7A5E14` | Small gold-toned text |
| Stone | `#5F5A4D` | Captions, metadata |
| Parchment | `#D9CDB0` | Rules and borders |
| Mist | `#E4DAC0` | Soft rules |
| Light Gold | `#D8B15A` | Gold on dark grounds |

Gold on ivory is 3.4 to 3.7:1. Use Heritage and Antique Gold for the logotype,
display type at 24 px and up, rules and icons. Set small gold-toned text in
Bronze Text (5.4:1). Ink on Heritage Gold is 4.2:1, so keep gold buttons to
bold text at 14 px or larger and prefer 18 px bold where space allows.

## Type

- **Display:** Fraunces 500/600, italic 400 for the one emphasized word. Draw
  display text at optical size 36 (`font-variation-settings: 'opsz' 36`) so it
  matches the logo.
- **Body:** IBM Plex Sans 400/500/600.
- **Labels:** IBM Plex Mono 400/500, caps with 0.18 to 0.32 em tracking for
  eyebrows.

The wordmark is Fraunces SemiBold, optical size 36, +10 tracking. "IvoryCoast"
is Ink Navy and "Advisory" is Antique Gold. The descriptor is IBM Plex Mono
Regular in caps at +260 tracking, set to the exact width of the wordmark.

Fonts are SIL Open Font License. Load them from Google Fonts:

```css
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..600;1,9..144,400..500&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
```
