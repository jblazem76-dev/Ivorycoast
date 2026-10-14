"""Procedural Calacatta-style marble for the hero medallion -> site/assets/fx/marble.webp
Ivory base, warm grey veining and a thin gold vein. Seeded, so output is reproducible.
Needs numpy and Pillow. Run from the repository root."""
import numpy as np
from PIL import Image, ImageFilter

N = 760
SEED = 7

def noise(seed, cells):
    rng = np.random.default_rng(seed)
    g = rng.random((cells + 3, cells + 3)).astype(np.float32)
    return np.asarray(Image.fromarray(g).resize((N, N), Image.BICUBIC), dtype=np.float32)

def fbm(seed, base, octaves=5, gain=0.5):
    out = np.zeros((N, N), np.float32); amp = 1.0; tot = 0.0
    for i in range(octaves):
        out += amp * noise(seed + i * 17, max(2, int(base * 2 ** i))); tot += amp; amp *= gain
    out /= tot
    lo, hi = np.percentile(out, 2), np.percentile(out, 98)
    return np.clip((out - lo) / (hi - lo), 0, 1)

def smooth(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)

def turb(seed, base, octaves=5):
    out = np.zeros((N, N), np.float32); amp = 1.0; tot = 0.0
    for i in range(octaves):
        out += amp * np.abs(noise(seed + i * 29, max(2, int(base * 2 ** i))) - 0.5) * 2; tot += amp; amp *= 0.55
    return out / tot

Y, X = np.mgrid[0:N, 0:N].astype(np.float32) / N
W1, W2, W3 = fbm(SEED, 3, 5), fbm(SEED + 100, 4, 4), fbm(SEED + 200, 2, 4)

T1, T2 = turb(SEED + 900, 4, 6), turb(SEED + 950, 7, 5)

def vein(theta, freq, warp, sharp, offset, seed):
    u = X * np.cos(theta) + Y * np.sin(theta)
    ph = u * freq + warp * (W1 - 0.5) + 0.22 * (T1 - 0.3) + 0.07 * (T2 - 0.3) + offset
    line = 1 - np.abs(np.sin(np.pi * ph))
    mod = smooth(fbm(seed, 2, 4), 0.30, 0.60)           # veins fade in and out along their length
    return line ** sharp, mod

# base stone: warm ivory with soft cloudy variation
c = smooth(fbm(SEED + 300, 2, 5), 0.2, 0.85)
base = np.array([247, 242, 232], np.float32) * (1 - c[..., None] * 0.7) + np.array([224, 216, 200], np.float32) * (c[..., None] * 0.7)
warm = smooth(fbm(SEED + 400, 3, 3), 0.55, 0.9)[..., None] * np.array([6, 2, -10], np.float32)
img = base + warm

# veins
m_thin, m_mod = vein(np.deg2rad(32), 1.5, 0.7, 40, 0.05, SEED + 500)
m_soft, _ = vein(np.deg2rad(32), 1.5, 0.7, 6, 0.05, SEED + 500)
m_cloud, _ = vein(np.deg2rad(32), 1.5, 0.7, 2.5, 0.05, SEED + 500)
a = np.clip(m_thin * 0.80 * m_mod + m_soft * 0.30 * m_mod + m_cloud * 0.10 * m_mod, 0, 1)[..., None]
img = img * (1 - a) + np.array([104, 96, 86], np.float32) * a

s_thin, s_mod = vein(np.deg2rad(-28), 1.7, 0.8, 55, 0.31, SEED + 600)
s_soft, _ = vein(np.deg2rad(-28), 1.7, 0.8, 8, 0.31, SEED + 600)
a = np.clip(s_thin * 0.60 * s_mod + s_soft * 0.22 * s_mod, 0, 1)[..., None]
img = img * (1 - a) + np.array([150, 138, 120], np.float32) * a

g_thin, g_mod = vein(np.deg2rad(52), 1.4, 0.9, 85, 0.62, SEED + 700)
g_soft, _ = vein(np.deg2rad(52), 1.4, 0.9, 12, 0.62, SEED + 700)
a = np.clip(g_thin * 0.85 * g_mod + g_soft * 0.20 * g_mod, 0, 1)[..., None]
img = img * (1 - a) + np.array([178, 136, 54], np.float32) * a

h_thin, h_mod = vein(np.deg2rad(14), 6.0, 1.2, 140, 0.2, SEED + 800)
a = np.clip(h_thin * 0.34 * h_mod, 0, 1)[..., None]
img = img * (1 - a) + np.array([132, 122, 108], np.float32) * a

# crystalline grain
rng = np.random.default_rng(SEED)
img += (rng.random((N, N, 1)).astype(np.float32) - 0.5) * 7
img += (np.asarray(Image.fromarray(rng.random((N // 3, N // 3)).astype(np.float32)).resize((N, N), Image.BICUBIC))[..., None] - 0.5) * 6

out = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB").filter(ImageFilter.GaussianBlur(0.55))
out.save("site/assets/fx/marble.webp", quality=88, method=6)
out.save("/tmp/marble_preview.png")
import os; print(os.path.getsize("site/assets/fx/marble.webp"))
