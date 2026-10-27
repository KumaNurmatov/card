"""Из исходных скринов WeChat (src/) делает img/<slug>.jpg: имя сверху, внизу компания и страна на EN/中文."""
import pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = pathlib.Path(__file__).parent
SF = "/System/Library/Fonts/SFNS.ttf"
CN = "/System/Library/Fonts/Hiragino Sans GB.ttc"

# slug, файл исходника, имя
CARDS = [
    ("kanykei", "kana.jpg", "Kanykei"),
    ("aigerim", "aika.jpg", "Aigerim"),
    ("rakhat", "rahat.jpg", "Rakhat"),
    ("erlan", "erlan.jpg", "Erlan"),
]

LINES = [  # текст, шрифт, доля ширины, цвет
    ("Ordo Trade Distribution Company", "sf-bold", 0.050, (17, 17, 17)),
    ("Kyrgyzstan", "sf", 0.042, (90, 90, 90)),
    ("Ordo Trade 分销公司", "cn-bold", 0.046, (17, 17, 17)),
    ("吉尔吉斯斯坦", "cn", 0.040, (90, 90, 90)),
]


def font(kind, size):
    if kind.startswith("cn"):
        return ImageFont.truetype(CN, size, index=2 if kind == "cn-bold" else 0)
    f = ImageFont.truetype(SF, size)
    f.set_variation_by_name("Bold" if kind == "sf-bold" else "Medium")
    return f


def build(slug, src, name):
    im = Image.open(OUT / "src" / src).convert("RGB")
    w, h = im.size
    g = np.array(im.convert("L")).astype(int)
    dark = np.where((g < 140).sum(1) > 5)[0]
    qr_bottom = dark.max()
    qr_top = dark[dark > h * 0.2].min()
    # аватарка: первая непустая колонка слева в шапке и её правый край
    head = g[60:qr_top - 40]
    cols = np.where((head < 250).sum(0) > 20)[0]
    av_left = cols.min()
    av_right = av_left
    while av_right + 1 in cols:  # аватарка — первый сплошной блок колонок
        av_right += 1
    rows = np.where((g[:, av_left:av_right] < 250).sum(1) > 20)[0]
    av_top, av_bot = rows.min(), rows[rows < qr_top - 40].max()

    d = ImageDraw.Draw(im)
    # шапка: стираем старое имя, пишем новое по центру высоты аватарки
    d.rectangle([av_right + 4, 40, w, qr_top - 30], fill="white")
    f = font("sf-bold", int(w * 0.058))
    bb = d.textbbox((0, 0), name, font=f)
    d.text((av_right + int(w * 0.03) - bb[0], (av_top + av_bot) // 2 - (bb[1] + bb[3]) // 2),
           name, font=f, fill=(17, 17, 17))

    # подвал
    top = qr_bottom + int(w * 0.05)
    d.rectangle([0, top, w, h], fill="white")
    gap = int(w * 0.018)
    items = []
    for text, kind, k, color in LINES:
        f = font(kind, int(w * k))
        bb = d.textbbox((0, 0), text, font=f)
        items.append((text, f, bb, color))
    total = sum(b[3] - b[1] for _, _, b, _ in items) + gap * (len(items) - 1) + gap  # доп. отступ между EN и CN
    y = top + ((h - top) - total) // 2
    for i, (text, f, bb, color) in enumerate(items):
        if i == 2:
            y += gap
        d.text(((w - (bb[2] - bb[0])) // 2 - bb[0], y - bb[1]), text, font=f, fill=color)
        y += bb[3] - bb[1] + gap
    im.save(OUT / "img" / f"{slug}.jpg", quality=92)


for slug, src, name in CARDS:
    build(slug, src, name)
    print(slug, "ok")
