import argparse
import logging
import time
import random
import requests

from config import (
    FJALEKYC_TECH,
    QYTETI_PARAZGJEDHJE,
    QARKU_PARAZGJEDHJE,
    VONESA_MIN,
    VONESA_MAX,
    SAVE_INTERVAL,
)
from scraper import kerko_subjekte, merr_flamuj, merr_dokument, nxirr_kontaktet
from ruajtja import ruaj_subjektet

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
log = logging.getLogger(__name__)


def prit():
    koha = random.uniform(VONESA_MIN, VONESA_MAX)
    time.sleep(koha)


def nderto_profil(i_paperpunuar: dict, flamuj: dict, kontaktet: dict) -> dict:
    return {
        "nipt": i_paperpunuar.get("nipti", ""),
        "emri_subjektit": i_paperpunuar.get("emriISubjektit", ""),
        "emri_tregtar": i_paperpunuar.get("emriTregtar", ""),
        "forma_ligjore": i_paperpunuar.get("formaLigjore", ""),
        "data_regjistrimit": i_paperpunuar.get("dataERegjistrimit", ""),
        "qyteti": i_paperpunuar.get("qyteti", ""),
        "pronesia": i_paperpunuar.get("shtetesia", ""),
        "statusi": i_paperpunuar.get("statusiISubjektit", ""),
        "aktiviteti": i_paperpunuar.get("sektoriIVeprimtarise", ""),
        "administrator_ortak": i_paperpunuar.get("adminOrtakAksionar", ""),
        "flamur_kuq": flamuj,
        "kontakti": kontaktet,
    }


def mblidh_subjekte(sesioni: requests.Session, fjalekyc_lista: list[str],
                     qyteti: str, qarku: str) -> dict[str, dict]:
    te_gjitha = {}

    for fjalekyc in fjalekyc_lista:
        rezultate = kerko_subjekte(sesioni, fjalekyc, qyteti, qarku)

        for subjekt in rezultate:
            nipt = subjekt.get("nipti", "")
            if nipt and nipt not in te_gjitha:
                te_gjitha[nipt] = subjekt

        if len(fjalekyc_lista) > 1:
            prit()

    log.info(f"Gjithsej {len(te_gjitha)} subjekte unike nga {len(fjalekyc_lista)} fjalekyc")
    return te_gjitha


def pasuro_subjektet(sesioni: requests.Session, subjekte: dict[str, dict],
                     shtegu_daljes: str) -> list[dict]:
    profile = []
    totali = len(subjekte)

    for i, (nipt, te_dhena) in enumerate(subjekte.items(), 1):
        emri = te_dhena.get("emriISubjektit", nipt)
        log.info(f"[{i}/{totali}] Po perpunohet: {emri} ({nipt})")

        flamuj = merr_flamuj(sesioni, nipt)
        prit()

        kontaktet = {"email": [], "telefon": []}
        pdf_base64 = merr_dokument(sesioni, nipt, lloji="simple")
        if pdf_base64:
            kontaktet = nxirr_kontaktet(pdf_base64, nipt)
            log.info(f"  -> {len(kontaktet['email'])} email, {len(kontaktet['telefon'])} telefon")
        else:
            log.warning(f"  -> Ska dokument PDF per {nipt}")

        profili = nderto_profil(te_dhena, flamuj, kontaktet)
        profile.append(profili)

        # Save periodically for crash recovery
        if i % SAVE_INTERVAL == 0:
            ruaj_subjektet(profile, shtegu_daljes)
            log.debug(f"Progresi u ruajt ({i}/{totali})")

        prit()

    return profile


def main():
    parser = argparse.ArgumentParser(description="Scraper per biznese shqiptare nga QKB")
    parser.add_argument("--fjalekyc", "-f", nargs="+", default=None,
                        help="Fjale kyce per kerkim (parazgjedhje: internet, software, IT, teknologji)")
    parser.add_argument("--qyteti", "-q", default=QYTETI_PARAZGJEDHJE,
                        help="Qyteti per kerkim")
    parser.add_argument("--qarku", "-r", default=QARKU_PARAZGJEDHJE,
                        help="Qarku per kerkim")
    parser.add_argument("--dalje", "-d", default="data/subjekte.json",
                        help="Shtegu i skedarit te daljes")
    parser.add_argument("--pa-pdf", action="store_true",
                        help="Kaperce shkarkimin e PDF (vetem kerkim + flamuj)")
    parser.add_argument("--debug", action="store_true",
                        help="Aktivizo debug logging")

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    fjalekyc = args.fjalekyc or FJALEKYC_TECH

    sesioni = requests.Session()

    log.info("Scraper QKB filloi")
    log.info(f"Fjalekyc: {fjalekyc}")
    log.info(f"Qyteti: {args.qyteti} | Qarku: {args.qarku}")

    subjekte = mblidh_subjekte(sesioni, fjalekyc, args.qyteti, args.qarku)

    if not subjekte:
        log.warning("Asnje subjekt u gjet, po dal")
        return

    if args.pa_pdf:
        log.info("Modaliteti pa-pdf: po kapercehen dokumentet PDF")
        profile = []
        for nipt, te_dhena in subjekte.items():
            flamuj = merr_flamuj(sesioni, nipt)
            prit()
            profili = nderto_profil(te_dhena, flamuj, {"email": [], "telefon": []})
            profile.append(profili)
    else:
        profile = pasuro_subjektet(sesioni, subjekte, args.dalje)

    ruaj_subjektet(profile, args.dalje)

    log.info(f"Perfundoi. {len(profile)} profile u ruajten ne {args.dalje}")


if __name__ == "__main__":
    main()
