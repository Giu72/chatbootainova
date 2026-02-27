import PyPDF2
import requests
from bs4 import BeautifulSoup

def carica_pdf(percorso):
    """Estrae testo da un file PDF."""
    testo = ""
    try:
        with open(percorso, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                testo += page.extract_text() or ""  # se None, metti stringa vuota
    except Exception as e:
        print(f"Errore nel caricamento del PDF: {e}")
    return testo

def carica_link(urls):
    """Scarica il testo da una lista di URL."""
    contenuto = ""
    for url in urls:
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            # Estrae solo testo visibile (senza script, style)
            for script in soup(["script", "style"]):
                script.decompose()
            contenuto += soup.get_text(separator="\n", strip=True)
        except Exception as e:
            print(f"Errore nel caricamento di {url}: {e}")
    return contenuto

# I tuoi link (rimossi gli spazi iniziali)
links = [
    "https://www.inps.it/it/it/sostegni-sussidi-indennita.html",
    "https://www.inps.it/it/it/sostegni-sussidi-indennita/per-disoccupati.html",
    "https://www.inps.it/it/it/lavoro/disoccupazione.html",
    "https://www.inps.it/it/it/servizi/per-i-cittadini/assegno-di-inclusione-adi",
    "https://www.inps.it/it/it/sostegni-sussidi-indennita/studio-e-formazione.html",
    "https://www.inps.it/it/it/sostegni-sussidi-indennita/per-nucleo-familiare.html",
    "https://www.inps.it/it/it/dettaglio-scheda.it.schede-servizio-strumento.schede-strumenti.assegno-per-il-nucleo-familiare-consultazione-degli-importi-anf-52810.assegno-per-il-nucleo-familiare-consultazione-degli-importi-anf.html",
    "https://www.inps.it/it/it/sostegni-sussidi-indennita/per-disabili-invalidi-inabili.html",
    "https://www.inps.it/it/it/previdenza/domanda-di-pensione.html",
    "https://www.inps.it/it/it/lavoro/contributi-dipendenti-e-collaboratori.html"
]

# Carica tutto una volta sola (utile per l'uso in app.py)
print("Caricamento documenti in corso...")
testo_pdf = carica_pdf("bilancio_2026.pdf")
testo_web = carica_link(links)
testo_totale = testo_pdf + "\n\n" + testo_web
print("Caricamento completato!")