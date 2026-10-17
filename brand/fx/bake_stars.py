import random
W, H = 808, 726
COLS = [("#ffffff", 50), ("#bcd4ff", 25), ("#ffc6e2", 12), ("#ffe2a8", 13)]
def pick():
    r = random.uniform(0, 100); acc = 0
    for c, w in COLS:
        acc += w
        if r <= acc: return c
    return "#ffffff"
def stars(seed, n, nebula=False):
    random.seed(seed)
    out = []
    if nebula:
        out.append('<defs>' + "".join(
            f'<radialGradient id="n{i}"><stop offset="0" stop-color="{c}" stop-opacity="{o}"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
            for i, (c, o) in enumerate([("#5a7cff", .16), ("#b86bff", .12), ("#ff8a4a", .09), ("#4fb3ff", .12), ("#ff6fb0", .08), ("#7a8cff", .14)])) + '</defs>')
        for i, (cx, cy, r) in enumerate([(300, 250, 230), (520, 220, 200), (410, 430, 240), (240, 440, 170), (590, 420, 190), (420, 150, 170)]):
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#n{i})"/>')
    for _ in range(n):
        x, y = random.uniform(0, W), random.uniform(0, H)
        t = random.random()
        col = pick()
        if t < 0.80:
            r = random.uniform(1.5, 2.7); o = random.uniform(.55, 1)
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{col}" fill-opacity="{o:.2f}"/>')
        elif t < 0.97:
            r = random.uniform(3, 4.8); o = random.uniform(.8, 1)
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{col}" fill-opacity="{o:.2f}"/>')
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*2.4:.2f}" fill="{col}" fill-opacity=".16"/>')
        else:
            r = random.uniform(5, 7); L = random.uniform(30, 52)
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*2.6:.2f}" fill="{col}" fill-opacity=".14"/>')
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="#fff"/>')
            out.append(f'<path d="M{x-L:.1f} {y:.1f}H{x+L:.1f}M{x:.1f} {y-L*0.8:.1f}V{y+L*0.8:.1f}" stroke="{col}" stroke-width="1.6" stroke-linecap="round" stroke-opacity=".85"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">' + "".join(out) + "</svg>\n"
open("site/assets/fx/stars-a.svg", "w").write(stars(11, 260, nebula=True))
open("site/assets/fx/stars-b.svg", "w").write(stars(97, 260))
import os; print(os.path.getsize("site/assets/fx/stars-a.svg"), os.path.getsize("site/assets/fx/stars-b.svg"))
