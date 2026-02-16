import os
import re
import base64
import logging

import pdfplumber

log = logging.getLogger(__name__)

REGEX_EMAIL = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
)

REGEX_TELEFON = re.compile(
    r"(?:\+355|00355|0)[\s\-]?\d{1,3}[\s\-]?\d{3,4}[\s\-]?\d{2,4}"
)

DIREKTORIA_PDF = os.path.join("data", "pdf")


def _dekodo_pdf(pdf_base64: str) -> bytes | None:
    try:
        i_pastruar = pdf_base64.strip()
        mbetja = len(i_pastruar) % 4
        if mbetja:
            i_pastruar += "=" * (4 - mbetja)
        return base64.b64decode(i_pastruar)
    except Exception as gabim:
        log.error(f"Gabim ne dekodimin e PDF base64: {gabim}")
        return None


def _ruaj_pdf(pdf_bytes: bytes, nipt: str) -> str:
    os.makedirs(DIREKTORIA_PDF, exist_ok=True)
    shtegu = os.path.join(DIREKTORIA_PDF, f"{nipt}.pdf")
    with open(shtegu, "wb") as skedar:
        skedar.write(pdf_bytes)
    return shtegu


def _fshi_pdf(shtegu: str):
    try:
        if os.path.exists(shtegu):
            os.remove(shtegu)
    except OSError as gabim:
        log.warning(f"Nuk u fshi PDF: {shtegu} - {gabim}")


def _nxirr_tekst_nga_pdf(shtegu: str) -> str:
    teksti_plote = []
    try:
        with pdfplumber.open(shtegu) as pdf:
            for faqe in pdf.pages:
                tekst = faqe.extract_text()
                if tekst:
                    teksti_plote.append(tekst)
    except Exception as gabim:
        log.error(f"Gabim ne leximin e PDF: {gabim}")
    return "\n".join(teksti_plote)


def _gjej_emaile(tekst: str) -> list[str]:
    emaile = REGEX_EMAIL.findall(tekst)
    emaile_unike = list(dict.fromkeys(e.lower() for e in emaile))
    return emaile_unike


def _gjej_telefona(tekst: str) -> list[str]:
    telefona = REGEX_TELEFON.findall(tekst)
    telefona_pastro = []
    for t in telefona:
        i_pastruar = re.sub(r"\s+", " ", t.strip())
        if i_pastruar not in telefona_pastro:
            telefona_pastro.append(i_pastruar)
    return telefona_pastro


def nxirr_kontaktet(pdf_base64: str, nipt: str) -> dict:
    pdf_bytes = _dekodo_pdf(pdf_base64)
    if not pdf_bytes:
        return {"email": [], "telefon": []}

    shtegu_pdf = _ruaj_pdf(pdf_bytes, nipt)
    log.debug(f"PDF u ruajt: {shtegu_pdf}")

    tekst = _nxirr_tekst_nga_pdf(shtegu_pdf)

    _fshi_pdf(shtegu_pdf)
    log.debug(f"PDF u fshi: {shtegu_pdf}")

    if not tekst:
        log.warning(f"PDF per {nipt} nuk ka tekst te nxjerrur")
        return {"email": [], "telefon": []}

    emaile = _gjej_emaile(tekst)
    telefona = _gjej_telefona(tekst)

    return {"email": emaile, "telefon": telefona}
