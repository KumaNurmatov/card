"""Генерирует 4 страницы-визитки WeChat для NFC-карт. Запуск: python build.py"""
import base64, io, pathlib
import qrcode

OUT = pathlib.Path(__file__).parent

PEOPLE = [
    ("kanykei", "Kanykei Kazieva", "+996501337773", "https://u.wechat.com/kL06xAvDP1k_1zNUNfM3YCA?s=2"),
    ("aigerim", "Aigerim Seiitkulova", "+996702310333", "https://u.wechat.com/kACGkHspZeiOskFzMlgjDVs?s=2"),
    ("rakhat", "Rakhat Omurbekova", "+996558635885", "https://u.wechat.com/kKAu59lm5xUceo-d2NAY1BM?s=2"),
    ("erlan", "Mr. Erlan Seiitkulov", "+996555474719", "https://u.wechat.com/kBADlaXMV_9ccnPWyneEu2g?s=2"),
]


def qr_png(data):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=16, border=3)
    qr.add_data(data)
    buf = io.BytesIO()
    qr.make_image(fill_color="black", back_color="white").save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def pretty(phone):
    d = phone[4:]
    return f"+996 {d[:3]} {d[3:6]} {d[6:]}"


TEMPLATE = open(OUT / "template.html", encoding="utf-8").read()

for slug, name, phone, url in PEOPLE:
    vcard = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL;TYPE=CELL:{phone}\nNOTE:WeChat {url}\nEND:VCARD\n"
    html = (TEMPLATE
            .replace("{{NAME}}", name)
            .replace("{{PHONE}}", phone)
            .replace("{{PHONE_PRETTY}}", pretty(phone))
            .replace("{{WA}}", phone.lstrip("+"))
            .replace("{{QR}}", qr_png(url))
            .replace("{{VCARD}}", base64.b64encode(vcard.encode()).decode())
            .replace("{{SLUG}}", slug))
    d = OUT / slug
    d.mkdir(exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")
    print(slug, "ok")
