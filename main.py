import argparse
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)


def kerko_pune(fjalekyc: list[str], vendndodhje: list[str], skedari_daljes: str):
    """Kerkon pune nga burime te ndryshme online."""
    log.info(f"Kerkimi fillon: {fjalekyc} ne {vendndodhje}")

    rezultate = []

    # TODO: merr te dhena nga duapune.com
    # TODO: merr te dhena nga njoftime.com
    # TODO: merr te dhena nga linkedin (shqiperi)

    if not rezultate:
        log.warning("Asnje rezultat akoma - scrapers nuk jane implementuar")
        return

    ruaj_rezultatet(rezultate, skedari_daljes)


def ruaj_rezultatet(rezultate: list[dict], shtegu: str):
    """Ruan rezultatet ne skedar JSON."""
    import json
    log.info(f"Po ruhen {len(rezultate)} rezultate ne {shtegu}")
    with open(shtegu, "w", encoding="utf-8") as skedar:
        json.dump(rezultate, skedar, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Scraper per pune shqiptare")
    parser.add_argument("--fjalekyc", "-f", nargs="+", help="Fjale kyce per kerkimin")
    parser.add_argument("--vendndodhje", "-v", nargs="+", default=["Tirane"],
                        help="Vendndodhjet per kerkim")
    parser.add_argument("--dalje", "-d", default="data/pune.json",
                        help="Shtegu i skedarit te daljes")
    parser.add_argument("--debug", action="store_true", help="Aktivizo debug logging")

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    log.info("Job scraper filloi")
    kerko_pune(args.fjalekyc, args.vendndodhje, args.dalje)
    log.info("Job scraper perfundoi")


if __name__ == "__main__":
    main()
