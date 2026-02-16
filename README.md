# job-scraper

Scraper per biznese shqiptare nga QKB (Qendra Kombetare e Biznesit). Kerkon subjekte tech ne regjistrin tregtar, merr te dhenat e tyre, shkarkon ekstraktin PDF dhe nxjerr kontaktet (email, telefon). Rezultatet ruhen ne JSON.

**Akoma ne zhvillim - disa pjese mund te mos funksionojne si duhet.**

## Struktura

```
job-scraper/
  main.py               - entry point, CLI, orkestrimi i gjithe procesit
  config.py             - URL-te, headers, fjalekyc, parametra
  scraper/
    __init__.py
    kerkimi.py          - kerkon subjekte ne QKB (POST form -> parse JSON nga HTML)
    detajet.py          - merr flamujt e kuq + dokumentin PDF per cdo NIPT
    nxjerresi.py        - dekodon PDF base64, nxjerr email/telefon me pdfplumber
  ruajtja/
    __init__.py
    json_ruajtje.py     - ruan profilet ne JSON, deduplikon me NIPT
  data/                 - ktu ruhen rezultatet
```

## Si ta nisesh

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Perdorimi

```bash
# kerkim me fjalekyc parazgjedhje (internet, software, IT, teknologji)
python main.py

# vetem nje fjalekyc specifike
python main.py -f software

# qytet tjeter
python main.py -q durres -r durres

# pa shkarkuar PDF (me shpejt, pa kontakte)
python main.py --pa-pdf

# debug logging
python main.py --debug

# output ne shteg tjeter
python main.py -d data/tech_tirane.json
```

Rezultatet ruhen ne `data/subjekte.json` si parazgjedhje.

## Si duket nje profil ne JSON

```json
{
  "nipt": "L51306027M",
  "emri_subjektit": "TIMBAST",
  "emri_tregtar": "TIMBAST",
  "forma_ligjore": "SHA",
  "data_regjistrimit": "06/01/2015",
  "qyteti": "Tirane",
  "pronesia": "E Perbashket (shqiptare - e huaj)",
  "statusi": "Aprovuar",
  "aktiviteti": "...",
  "administrator_ortak": "Alban Mesonjesi;...",
  "flamur_kuq": {
    "rpp": "",
    "bilanci": "Subjekti nuk ka depozituar...",
    "admin": "Afati i emerimit...",
    "ka_flamur": true
  },
  "kontakti": {
    "email": ["info@example.al"],
    "telefon": ["+355 4 123 4567"]
  }
}
```

## Cfare mbetet

- Mbulim per qytete te tjera pervec Tiranes
- Fjalekyc me te gjera per industri te tjera
- Eksport ne formate te tjera (CSV, Excel)
- Retry logic per kerkesa qe deshtojne

## Shenim

Vetem per perdorim personal. Kerkesa behen me 1-2 sekonda vonese mes tyre qe te mos ngarkojme serverin e QKB.
