# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFilter
import math

W = H = 1080
CREAM   = (250, 247, 238)
GREEN_D = (35, 79, 47)
GREEN   = (74, 122, 74)
GREEN_L = (140, 176, 116)
ORANGE  = (226, 132, 19)
ORANGE_D= (198, 106, 32)
WHITE   = (255, 255, 255)

FROB = "/home/appuser/.local/lib/python3.12/site-packages/font_roboto/files/"
def F(name):
    from PIL import ImageFont
    return ImageFont.truetype(FROB + name, 10)

from PIL import ImageFont
def font(name, size):
    return ImageFont.truetype(FROB + name, size)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# gradient background
top = (252, 249, 241); bot = (228, 238, 216)
step_img = Image.new("RGB", (1, H))
for y in range(H):
    t = y / H
    step_img.putpixel((0, y), tuple(int(a + (b - a) * t) for a, b in zip(top, bot)))
img.paste(step_img.resize((W, H)), (0, 0))

# soft decorative blobs
blob = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(blob)
bd.ellipse([-260, -260, 240, 240], fill=(74, 122, 74, 40))
bd.ellipse([860, -180, 1220, 180], fill=(226, 132, 19, 46))
bd.ellipse([-140, 380, 180, 700], fill=(140, 176, 116, 40))
blob = blob.filter(ImageFilter.GaussianBlur(60))
img.paste(blob, (0, 0), blob)
d = ImageDraw.Draw(img)

# ---------- gardenillustration band ----------
def bezier(p0, p1, p2, n=60):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t**2*p2[0]
        y = (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t**2*p2[1]
        pts.append((x, y))
    return pts

BASE = 700
# back hill
hb = bezier((0, 560), (300, 470), (560, 560)) + bezier((560, 560), (820, 645), (1080, 560)) + [(1080, BASE+40), (0, BASE+40)]
d.polygon(hb, fill=(168, 199, 152))
# mid hill
hm = bezier((0, 630), (260, 545), (540, 630)) + bezier((540, 630), (830, 712), (1080, 630)) + [(1080, BASE+40), (0, BASE+40)]
d.polygon(hm, fill=(112, 152, 100))
# front lawn
hf = bezier((0, 712), (360, 660), (720, 712)) + bezier((720, 712), (920, 750), (1080, 712)) + [(1080, BASE+45), (0, BASE+45)]
d.polygon(hf, fill=(84, 128, 80))

# sun
sx, sy, sr = 905, 175, 62
for r, a in ((sr+26, 60), (sr+12, 90)):
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    gd.ellipse([sx-r-16, sy-r-16, sx+r+16, sy+r+16] if r == sr+26 else [sx-r, sy-r, sx+r, sy+r], fill=(243, 178, 78, a))
    img.paste(gl, (0, 0), gl)
d.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(244, 186, 96))

def bush(cx, cy, w, h, col):
    pts = bezier((cx-w, cy), (cx-w*0.6, cy-h), (cx, cy-h*0.86)) + \
          bezier((cx, cy-h*0.86), (cx+w*0.6, cy-h), (cx+w, cy))
    d.polygon(pts + [(cx+w, cy), (cx-w, cy)], fill=col)

# trees
def tree(cx, gy, sc, leaf, dark):
    r = 44*sc
    tx, ty = cx, gy
    d.rectangle([tx-5*sc, ty-r*0.6, tx+5*sc, ty+6*sc], fill=(122, 88, 56))
    for dx, dy, rr, c in ((0, -r*1.2, r, leaf), (-r*0.72, -r*0.55, r*0.72, dark), (r*0.72, -r*0.55, r*0.72, dark)):
        d.ellipse([tx+dx-rr, ty+dy-rr, tx+dx+rr, ty+dy+rr], fill=c)

tree(150, 640, 1.05, (58, 104, 62), (74, 122, 74))
tree(985, 655, 0.8, (58, 104, 62), (74, 122, 74))
bush(420, 660, 90, 78, (96, 140, 88))
bush(560, 668, 70, 58, (120, 160, 104))
bush(800, 662, 100, 84, (96, 140, 88))

# flowers
def flower(fx, fy, pc, cc):
    for ang in range(0, 360, 72):
        px = fx + 9*math.cos(math.radians(ang)); py = fy + 9*math.sin(math.radians(ang))
        d.ellipse([px-6, py-6, px+6, py+6], fill=pc)
    d.ellipse([fx-4, fy-4, fx+4, fy+4], fill=cc)
for fx, fy, col in ((250, 740, (232, 156, 42)), (330, 762, (214, 92, 60)), (660, 752, (232, 156, 42)),
                    (740, 775, (214, 92, 60)), (900, 745, (232, 156, 42)), (90, 758, (214, 92, 60)),
                    (500, 780, (232, 156, 42))):
    flower(fx, fy, col, (196, 84, 34))

# ---------- header ----------
title = "LUBIN JARDINS"
f_title = font("Roboto-Bold.ttf", 88)
tw = d.textlength(title, font=f_title)
space_add = (720 - tw) / max(len(title)-1, 1)
x = (W - tw) / 2
d.text((x, 62), title, font=f_title, fill=GREEN_D)
# letter-spread not needed; keep simple centered
d.text(((W - tw)/2, 62), title, font=f_title, fill=GREEN_D)

# leaf ornament
lx, ly = W/2, 195
for s in (-1, 1):
    lp = [(lx, ly)]
    for i in range(1, 26):
        t = i / 25
        px = lx + s * 70 * math.sin(t * math.pi/2)
        py = ly - 26 * math.sin(t * math.pi)
        lp.append((px, py))
    d.line(lp, fill=GREEN, width=5)
for s in (-1, 1):
    sp = bezier((lx + s*14, ly-8), (lx + s*40, ly-30), (lx + s*62, ly-22))
    d.line(sp, fill=GREEN, width=3)

sub = "Création & entretien de vos espaces verts"
f_sub = font("Roboto-Medium.ttf", 34)
d.text(((W - d.textlength(sub, font=f_sub))/2, 218), sub, font=f_sub, fill=(96, 78, 50))

# ---------- services card ----------
card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(card)
cd.rounded_rectangle([115, 400, 965, 855], radius=38, fill=(255, 255, 255, 216))
card = card.filter(ImageFilter.GaussianBlur(0.6))
img.paste(card, (0, 0), card)
d = ImageDraw.Draw(img)

svcs = [
    ("Entretien de jardins", "Tonte, taille de haies, entretien régulier"),
    ("Élagage & clôtures", "Élagage, débroussaillage, pose de clôtures"),
    ("Aménagement & potagers", "Création de jardins et potagers sur mesure"),
    ("Arrosage & irrigation", "Pose de systèmes d'irrigation automatique"),
]
f_h = font("Roboto-Bold.ttf", 33)
f_t = font("Roboto-Regular.ttf", 25)
y = 430
for h1, t2 in svcs:
    # orange leaf bullet
    d.ellipse([150, y+8, 186, y+44], fill=(226, 132, 19, 30))
    d.ellipse([150, y+8, 186, y+44], outline=ORANGE, width=3)
    d.ellipse([165, y+16, 180, y+36], fill=GREEN)
    d.text((215, y+2), h1, font=f_h, fill=GREEN_D)
    d.text((215, y+46), t2, font=f_t, fill=(110, 105, 90))
    y += 106

# devis badge
bw, bx, by = 246, 768, 352
d.ellipse([bx, by, bx+bw, by+bw], fill=ORANGE)
d.ellipse([bx+10, by+10, bx+bw-10, by+bw-10], outline=WHITE, width=3)
f_bad = font("Roboto-Bold.ttf", 40)
d.text((bx + (bw - d.textlength("Devis", font=f_bad))/2, by+72), "Devis", font=f_bad, fill=WHITE)
d.text((bx + (bw - d.textlength("gratuit", font=f_bad))/2, by+128), "gratuit", font=f_bad, fill=WHITE)

# ---------- footer ----------
foot = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fd = ImageDraw.Draw(foot)
fd.rounded_rectangle([-40, 880, W+40, H+40], radius=60, fill=(35, 79, 47, 255))
img.paste(foot, (0, 0), foot)
d = ImageDraw.Draw(img)

tag = "« Donnons vie à votre jardin »"
f_tag = font("Roboto-Italic.ttf", 27)
d.text(((W - d.textlength(tag, font=f_tag))/2, 896), tag, font=f_tag, fill=(214, 226, 198))
d.line([W/2-90, 940, W/2+90, 940], fill=ORANGE, width=3)

f_c1 = font("Roboto-Bold.ttf", 36)
c1 = "06 83 26 13 54"
c2 = "cedriclubinolivier@hotmail.com"
f_c2 = font("Roboto-Medium.ttf", 28)
gap = 70
w_tot = d.textlength(c1, font=f_c1) + gap + d.textlength(c2, font=f_c2)
x1 = (W - w_tot)/2
d.text((x1, 962), c1, font=f_c1, fill=WHITE)
x2 = x1 + d.textlength(c1, font=f_c1) + gap
d.text((x2, 966), c2, font=f_c2, fill=(222, 234, 210))

# pin icon + zone
zone = "Intervention en Haute-Garonne et alentours"
f_z = font("Roboto-Regular.ttf", 24)
zx = (W - d.textlength(zone, font=f_z))/2
d.text((zx, 1022), zone, font=f_z, fill=(196, 212, 180))

img.save("/workspace/lubinjardins/lubinjardins_flyer_1080x1080.png", quality=95)
print("saved")
