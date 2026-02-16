import re
import json
import logging
import requests

from config import URL_KERKIMI, HEADERS, FUSHAT_KERKIMIT

log = logging.getLogger(__name__)


def _nderto_payload(fjalekyc: str, qyteti: str, qarku: str) -> dict:
    payload = dict(FUSHAT_KERKIMIT)
    payload["sektoriIVeprimtarise"] = fjalekyc
    payload["qyteti"] = qyteti
    payload["qarku"] = qarku
    return payload


def _nxirr_json_nga_html(html: str) -> list[dict]:
    pattern = r'response\s*=\s*JSON\.parse\("(.+?)"\);'
    perkim = re.search(pattern, html, re.DOTALL)
    if not perkim:
        log.warning("Nuk u gjet JSON ne pergjigjen HTML")
        return []

    blob_raw = perkim.group(1)

    try:
        tekst_i_dekoduar = json.loads('"' + blob_raw + '"')
        te_dhena = json.loads(tekst_i_dekoduar)
    except json.JSONDecodeError as gabim:
        log.error(f"Gabim ne parsimin e JSON: {gabim}")
        return []

    return te_dhena


def kerko_subjekte(sesioni: requests.Session, fjalekyc: str, qyteti: str, qarku: str) -> list[dict]:
    payload = _nderto_payload(fjalekyc, qyteti, qarku)
    log.info(f"Kerkim: fjalekyc='{fjalekyc}' qyteti='{qyteti}' qarku='{qarku}'")

    try:
        pergjigje = sesioni.post(URL_KERKIMI, data=payload, headers=HEADERS, timeout=30)
        pergjigje.raise_for_status()
    except requests.RequestException as gabim:
        log.error(f"Gabim ne kerkese: {gabim}")
        return []

    subjekte = _nxirr_json_nga_html(pergjigje.text)
    log.info(f"U gjeten {len(subjekte)} subjekte per '{fjalekyc}'")
    return subjekte
