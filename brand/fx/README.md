# Hero crest effect: source

The hero crest's lighting is baked into `site/assets/fx/`; the motion is CSS in
`site/index.html`.

- `bake_rim.py` builds `rim.webp`, the directional warm rim light and bloom,
  from the crest silhouette (`brand/logo/png/mark-navy.png`). Needs numpy and Pillow.
- `bake_stars.py` writes `stars-a.svg` and `stars-b.svg`, the two starfields that
  cross-fade (twinkle) through the crest. Seeded, so output is reproducible.
- `mark-fx.svg` is the crest with its navy fills deepened so the stars read; it is
  `brand/logo/svg/mark.svg` with the fill colors remapped, linework and gold unchanged.
- `silhouette.svg` (copy of `mark-navy.svg`) is the CSS mask that confines the
  starfield, shimmer and shading to the crest.

Run from the repository root: `python3 brand/fx/bake_rim.py` and
`python3 brand/fx/bake_stars.py`.
