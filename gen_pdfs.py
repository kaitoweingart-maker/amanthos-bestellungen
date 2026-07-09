#!/usr/bin/env python3
"""Erzeugt ausfüllbare PDF-Bestellformulare (AcroForm) für Amanthos."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas

PAGE_W, PAGE_H = A4
MARGIN = 40
DARK = HexColor("#1a1a2e")
GOLD = HexColor("#b8963e")
GREY = HexColor("#666666")
LIGHT = HexColor("#f2f0eb")

ORDER_EMAIL = "kaito.weingart@amanthos.com"

FORMS = {
    "bestellung-fruehstueck": {
        "title": "Bestellformular – Frühstück",
        "items": [
            "Gipfeli", "Buttergipfel TK", "Tischbrötli TK", "Brot / Brötchen",
            "Toastbrot", "Rührei-Mix 1kg (EIFIX)", "Butter", "Butter-Portionen 10g",
            "Konfitüre", "Portionenkonfitüre", "Honig", "Käse", "Fleisch-Aufschnitt",
            "Joghurt", "Müsli / Cornflakes", "Milch", "Orangensaft", "Eier",
            "Früchte", "Zucker / Süssstoff",
        ],
        "extra_rows": 4,
    },
    "bestellung-reinigungsmaterial": {
        "title": "Bestellformular – Reinigungsmaterial",
        "items": [
            "Allzweckreiniger", "Badreiniger / Kalklöser", "WC-Reiniger",
            "Glasreiniger", "Bodenreiniger", "Geschirrspülmittel",
            "Geschirrspültabs", "Waschmittel", "Abfallsäcke 35 l",
            "Abfallsäcke 110 l", "Putzhandschuhe", "Schwämme",
            "Mikrofasertücher", "WC-Papier", "Haushaltspapier", "Handseife",
            "Kosmetiktücher", "Duschgel-Sachets 12ml", "All-in-One Duschmittel 300ml",
            "Seife Flowpack", "Vanity-Set (Wattepads)", "Spenderservietten",
        ],
        "extra_rows": 4,
    },
    "bestellung-kaffee": {
        "title": "Bestellformular – Kaffee & Tee",
        "items": [
            "Turm Mokka Bohnen 1kg", "CoffeeB Balls Lungo", "CoffeeB Balls Espresso",
            "Tee-Sortiment", "Kaffeerahm-Portionen", "Zucker-Sticks",
        ],
        "extra_rows": 6,
    },
    "bestellung-waesche": {
        "title": "Bestellformular – Wäsche",
        "items": [
            "Fixleintuch 90 × 200", "Fixleintuch 160 × 200",
            "Fixleintuch 180 × 200", "Duvetbezug 160 × 210",
            "Duvetbezug 200 × 210", "Kissenbezug 65 × 65",
            "Kissenbezug 50 × 70", "Duvet", "Kissen",
            "Badetücher", "Handtücher", "Gästetücher",
            "Badteppiche", "Küchentücher",
        ],
        "extra_rows": 4,
    },
}

# Spalten: Artikel | Menge | Preis CHF | Bezahlt
COL_X = [MARGIN, 320, 400, 480, PAGE_W - MARGIN]
ROW_H = 24


def header(c, title):
    c.setFillColor(DARK)
    c.rect(0, PAGE_H - 90, PAGE_W, 90, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(MARGIN, PAGE_H - 55, title)
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN, PAGE_H - 74, "Amanthos AG · Früemattli 1 · 6404 Greppen")


def meta_fields(c, prefix):
    y = PAGE_H - 130
    fields = [("Objekt / Standort", "objekt", 200), ("Besteller/in", "besteller", 150),
              ("Datum", "datum", 90)]
    x = MARGIN
    c.setFont("Helvetica", 9)
    for label, name, w in fields:
        c.setFillColor(GREY)
        c.drawString(x, y + 22, label)
        c.acroForm.textfield(
            name=f"{prefix}_{name}", x=x, y=y, width=w, height=18,
            borderColor=GREY, fillColor=white, textColor=black,
            fontSize=10, borderWidth=0.5)
        x += w + 18


def table_header(c, y):
    c.setFillColor(LIGHT)
    c.rect(MARGIN, y - 6, PAGE_W - 2 * MARGIN, ROW_H, stroke=0, fill=1)
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(COL_X[0] + 4, y, "Artikel")
    c.drawString(COL_X[1] + 4, y, "Menge")
    c.drawString(COL_X[2] + 4, y, "Preis CHF")
    c.drawString(COL_X[3] + 4, y, "Bezahlt")


def footer(c):
    c.setFont("Helvetica", 9)
    c.setFillColor(GREY)
    c.drawString(MARGIN, 46, f"Bitte ausgefülltes Formular senden an: {ORDER_EMAIL}")
    c.drawString(MARGIN, 33, "Offene Positionen (Spalte «Bezahlt» leer) werden durch die Buchhaltung beglichen.")


def build(slug, cfg):
    c = canvas.Canvas(f"pdf/{slug}.pdf", pagesize=A4)
    c.setTitle(cfg["title"])
    c.setAuthor("Amanthos AG")
    header(c, cfg["title"])
    meta_fields(c, slug)

    y = PAGE_H - 175
    table_header(c, y)
    y -= ROW_H

    rows = [(i, name) for i, name in enumerate(cfg["items"])]
    rows += [(len(rows) + i, None) for i in range(cfg["extra_rows"])]

    c.setFont("Helvetica", 10)
    for i, name in rows:
        if y < 70:  # Seitenumbruch
            footer(c)
            c.showPage()
            header(c, cfg["title"] + " (Fortsetzung)")
            y = PAGE_H - 130
            table_header(c, y)
            y -= ROW_H
            c.setFont("Helvetica", 10)
        c.setStrokeColor(HexColor("#dddddd"))
        c.setLineWidth(0.5)
        c.line(MARGIN, y - 6, PAGE_W - MARGIN, y - 6)
        if name:
            c.setFillColor(black)
            c.drawString(COL_X[0] + 4, y, name)
        else:
            c.acroForm.textfield(
                name=f"{slug}_artikel_{i}", x=COL_X[0] + 2, y=y - 4,
                width=COL_X[1] - COL_X[0] - 10, height=16,
                borderColor=HexColor("#cccccc"), fillColor=white,
                textColor=black, fontSize=9, borderWidth=0.5)
        c.acroForm.textfield(
            name=f"{slug}_menge_{i}", x=COL_X[1] + 2, y=y - 4, width=60, height=16,
            borderColor=HexColor("#cccccc"), fillColor=white, textColor=black,
            fontSize=9, borderWidth=0.5)
        c.acroForm.textfield(
            name=f"{slug}_preis_{i}", x=COL_X[2] + 2, y=y - 4, width=60, height=16,
            borderColor=HexColor("#cccccc"), fillColor=white, textColor=black,
            fontSize=9, borderWidth=0.5)
        c.acroForm.checkbox(
            name=f"{slug}_bezahlt_{i}", x=COL_X[3] + 18, y=y - 3, size=13,
            borderColor=GREY, fillColor=white, textColor=black, borderWidth=0.75)
        y -= ROW_H

    # Bemerkungen
    if y < 130:
        footer(c)
        c.showPage()
        header(c, cfg["title"] + " (Fortsetzung)")
        y = PAGE_H - 130
    c.setFillColor(GREY)
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, y - 4, "Bemerkungen")
    c.acroForm.textfield(
        name=f"{slug}_bemerkungen", x=MARGIN, y=y - 60, width=PAGE_W - 2 * MARGIN,
        height=50, borderColor=GREY, fillColor=white, textColor=black,
        fontSize=10, borderWidth=0.5, fieldFlags="multiline")

    footer(c)
    c.save()
    print(f"pdf/{slug}.pdf")


for slug, cfg in FORMS.items():
    build(slug, cfg)
