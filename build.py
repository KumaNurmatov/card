"""Генерирует 4 страницы-визитки WeChat для NFC-карт. Картинки — img/<slug>.jpg. Запуск: python build.py"""
import pathlib

OUT = pathlib.Path(__file__).parent

PEOPLE = [
    ("kanykei", "Kanykei", "+996501337773"),
    ("aigerim", "Aigerim", "+996702310333"),
    ("rakhat", "Rakhat", "+996558635885"),
    ("erlan", "Erlan", "+996555474719"),
]

TEMPLATE = open(OUT / "template.html", encoding="utf-8").read()

for slug, name, phone in PEOPLE:
    html = (TEMPLATE
            .replace("{{NAME}}", name)
            .replace("{{WA}}", phone.lstrip("+"))
            .replace("{{SLUG}}", slug))
    (OUT / slug / "index.html").write_text(html, encoding="utf-8")
    print(slug, "ok")
