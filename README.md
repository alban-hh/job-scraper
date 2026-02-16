# job-scraper

Scraper per pune shqiptare. Merr te dhena nga faqe te ndryshme pune si duapune.com, njoftime.com, etj. dhe i ruan ne JSON per analiz.

**Projekti eshte akoma ne fazen fillestare - kjo qe sheh ktu eshte vetem skeleti baze. Asgje nuk funksionon akoma.**

## Struktura

```
job-scraper/
  main.py            - skripta kryesore
  requirements.txt   - dependencies
  data/              - ktu ruhen rezultatet
```

## Si ta nisesh

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Perdorimi

```bash
# kerkim baze
python main.py --fjalekyc developer python

# kerkim me vendndodhje specifike
python main.py --fjalekyc developer --vendndodhje Tirane Durres

# me debug logging
python main.py --fjalekyc developer --debug
```

Rezultatet ruhen ne `data/pune.json` si parazgjedhje. Mund ta ndryshosh me `--dalje shtegu/tjeter.json`.

## Cfare mbetet per tu bere

- Scraper per duapune.com
- Scraper per njoftime.com
- Filtrim me i avancuar i rezultateve
- Rate limiting qe te mos bllokohemi

## Shenim

Kjo eshte vetem per perdorim personal. Ki kujdes me terms of service te faqeve qe scrapon.
