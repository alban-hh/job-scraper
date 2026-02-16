import logging
import requests

from config import URL_FLAMUJ, URL_DOKUMENT, HEADERS

log = logging.getLogger(__name__)


def merr_flamuj(sesioni: requests.Session, nipt: str) -> dict:
    try:
        pergjigje = sesioni.post(
            URL_FLAMUJ,
            data={"nipt": nipt},
            headers=HEADERS,
            timeout=15,
        )
        pergjigje.raise_for_status()
        te_dhena = pergjigje.json()
    except (requests.RequestException, ValueError) as gabim:
        log.error(f"Gabim ne marrjen e flamujve per {nipt}: {gabim}")
        return {}

    if te_dhena.get("status") != 1:
        log.warning(f"Pergjigje e papritur per flamujt e {nipt}")
        return {}

    flamuj = te_dhena.get("data", {})
    return {
        "rpp": flamuj.get("rppRedFlagText", ""),
        "bilanci": flamuj.get("bilanciRedFlagText", ""),
        "admin": flamuj.get("adminRedFlagText", ""),
        "ka_flamur": flamuj.get("showRedFlag", False),
    }


def merr_dokument(sesioni: requests.Session, nipt: str, lloji: str = "simple") -> str | None:
    try:
        pergjigje = sesioni.post(
            URL_DOKUMENT,
            data={"nipt": nipt, "docType": lloji},
            headers=HEADERS,
            timeout=60,
        )
        pergjigje.raise_for_status()
        te_dhena = pergjigje.json()
    except (requests.RequestException, ValueError) as gabim:
        log.error(f"Gabim ne shkarkimin e dokumentit per {nipt}: {gabim}")
        return None

    if te_dhena.get("status") != 1:
        log.warning(f"Dokumenti per {nipt} nuk u gjet (status != 1)")
        return None

    pdf_base64 = te_dhena.get("data", "")
    if not pdf_base64 or len(pdf_base64) < 100:
        log.warning(f"Dokumenti per {nipt} eshte bosh ose shume i shkurter")
        return None

    return pdf_base64
