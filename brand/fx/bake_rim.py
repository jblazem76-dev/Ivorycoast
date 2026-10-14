import numpy as np
from PIL import Image, ImageFilter

SRC = "brand/logo/png/mark-navy.png"   # 1200 wide silhouette, line gaps knocked out
W_OUT = 660
a = Image.open(SRC).convert("RGBA").split()[3]
W, H = a.size
PADX, PADY = 60, 54
# close the facet-line gaps so we light the OUTER silhouette only
c = a.filter(ImageFilter.MaxFilter(23)).filter(ImageFilter.MinFilter(23))
S = np.asarray(c, dtype=np.float32) / 255.0
canvas = np.zeros((H + 2 * PADY, W + 2 * PADX), np.float32)
canvas[PADY:PADY + H, PADX:PADX + W] = S
def shift(m, dx, dy):
    out = np.zeros_like(m)
    h, w = m.shape
    xs, xe = max(dx, 0), w + min(dx, 0)
    ys, ye = max(dy, 0), h + min(dy, 0)
    out[ys:ye, xs:xe] = m[ys - dy:ye - dy, xs - dx:xe - dx]
    return out
def blur(m, r):
    im = Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(r)), dtype=np.float32) / 255.0

d = 8
warm = np.clip(canvas - shift(canvas, d, int(d * 0.85)), 0, 1)          # edges facing top-left
cool = np.clip(canvas - shift(canvas, -d, -int(d * 0.85)), 0, 1)        # opposite edge, fainter and cooler
core = blur(warm, 1.4)
bloom = 0.9 * blur(warm, 9) + 0.55 * blur(warm, 26) + 0.18 * blur(warm, 60)
inside = blur(canvas, 1.2)
# bloom lives outside the silhouette (a little spills in at the lit edge); the interior stays dark
bloom = bloom * (1 - 0.92 * inside) + 0.25 * bloom * inside
I = np.clip(core * 1.25 + bloom, 0, 1.6)

def ramp(i):
    # 0 -> clear, low -> deep orange, mid -> gold, high -> white-hot
    stops = np.array([0.0, 0.18, 0.55, 1.0, 1.6])
    cols = np.array([[0, 0, 0], [255, 96, 20], [255, 172, 64], [255, 236, 190], [255, 252, 240]], np.float32)
    out = np.stack([np.interp(i, stops, cols[:, k]) for k in range(3)], -1)
    return out
rgb = ramp(I)
A = np.clip(I * 1.05, 0, 1)

# cool secondary rim
ci = np.clip(blur(cool, 1.6) * 0.8 + 0.5 * blur(cool, 12), 0, 1) * 0.55
cool_rgb = np.stack([np.full_like(ci, 120), np.full_like(ci, 170), np.full_like(ci, 255)], -1)
# merge with 'screen' on color, union on alpha
a_tot = 1 - (1 - A) * (1 - ci)
rgb_tot = np.where(a_tot[..., None] > 0, (rgb * A[..., None] + cool_rgb * ci[..., None]) / np.maximum(a_tot[..., None], 1e-4), 0)

# chromatic fringe: nudge red outward, blue inward by 2px
def shift_ch(ch, dx, dy): return shift(ch, dx, dy)
rgb_tot[..., 0] = shift_ch(rgb_tot[..., 0], -2, -2)
rgb_tot[..., 2] = shift_ch(rgb_tot[..., 2], 2, 2)
img = np.dstack([np.clip(rgb_tot, 0, 255), np.clip(a_tot, 0, 1) * 255]).astype(np.uint8)
im = Image.fromarray(img, "RGBA")
h_out = round(W_OUT * im.height / im.width)
im = im.resize((W_OUT, h_out), Image.LANCZOS)
im.save("/tmp/rim.png")
im.save("site/assets/fx/rim.webp", quality=82, method=6)
print(im.size)
import os; print(os.path.getsize("/tmp/rim.png"), os.path.getsize("site/assets/fx/rim.webp"))
