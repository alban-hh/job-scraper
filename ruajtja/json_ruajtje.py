import os
import json
import logging

log = logging.getLogger(__name__)


def ruaj_subjektet(subjekte: list[dict], shtegu: str):
    direktoria = os.path.dirname(shtegu)
    if direktoria and not os.path.exists(direktoria):
        os.makedirs(direktoria, exist_ok=True)

    ekzistuese = {}
    if os.path.exists(shtegu):
        try:
            with open(shtegu, "r", encoding="utf-8") as skedar:
                lista = json.load(skedar)
                for s in lista:
                    if isinstance(s, dict) and "nipt" in s:
                        ekzistuese[s["nipt"]] = s
        except json.JSONDecodeError as gabim:
            log.warning(f"Skedari ekzistues {shtegu} nuk u lexua ({gabim}), do ta mbishkruaj")

    for s in subjekte:
        if isinstance(s, dict) and "nipt" in s:
            ekzistuese[s["nipt"]] = s
        else:
            if isinstance(s, dict):
                emri = s.get('emri_subjektit', 'I panjohur')
                log.warning(f"Subjekt pa NIPT u injorua: {emri}")
            else:
                log.warning(f"Subjekt me tip te pavlefshem u injorua: {type(s).__name__}")

    lista_perfundimtare = list(ekzistuese.values())
    lista_perfundimtare.sort(key=lambda x: x.get("emri_subjektit", ""))

    with open(shtegu, "w", encoding="utf-8") as skedar:
        json.dump(lista_perfundimtare, skedar, ensure_ascii=False, indent=2)

    log.info(f"U ruajten {len(lista_perfundimtare)} subjekte ne {shtegu}")
