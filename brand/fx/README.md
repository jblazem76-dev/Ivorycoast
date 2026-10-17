# Hero medallion: source

The hero is a polished marble disc with the crest inlaid. The marble and the
starfield are baked into `site/assets/fx/`; the gloss, bevel and shadows are CSS
in `site/index.html`; the random sparkles are a short script at the end of the page.

- `bake_marble.py` builds `marble.webp`, an ivory Calacatta-style marble with warm
  grey veining and thin gold veins, from seeded noise (reproducible). Needs numpy
  and Pillow.
- `bake_stars.py` writes `stars-a.svg` and `stars-b.svg`, the two starfields that
  cross-fade (twinkle) through the crest. Seeded, so output is reproducible.
- `mark-fx.svg` is the crest with its navy fills deepened so the stars read; it is
  `brand/logo/svg/mark.svg` with the fill colors remapped, linework and gold unchanged.
- `silhouette.svg` (copy of `mark-navy.svg`) is the CSS mask that confines the
  starfield and shading to the crest, and the shape the script samples so sparkles
  land only on the elephant.

Run from the repository root: `python3 brand/fx/bake_marble.py` and
`python3 brand/fx/bake_stars.py`. To change the marble, adjust `SEED` or the vein
settings in `bake_marble.py`.
