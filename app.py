import streamlit as st
import google.generativeai as genai
from cervello import testo_totale
import time

# ---------------------------
# 1. Configurazione pagina
# ---------------------------
st.set_page_config(page_title="Sportello Speed - Assistente Digitale", page_icon="⚡")
st.title("⚡ Sportello Speed: il tuo consulente per diritti e sussidi")
st.markdown("Hai dubbi su NASpI, ADI, Legge di Bilancio 2026 o altre pratiche INPS? Chiedi pure: ti guido io, passo passo.")

# ---------------------------
# 2. Configurazione AI con secrets
# ---------------------------
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("🔑 Chiave API non trovata. Crea il file `.streamlit/secrets.toml` con GOOGLE_API_KEY.")
    st.stop()

genai.configure(api_key=api_key, transport='rest')

# Modello aggiornato (se vuoi cambiare, modifica qui)
MODEL_NAME = 'gemini-2.5-flash'  # o 'gemini-3-flash-preview'
model = genai.GenerativeModel(MODEL_NAME)

# ---------------------------
# 3. Gestione cronologia chat
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------
# 4. Input utente e risposta
# ---------------------------
if prompt := st.chat_input("Scrivi qui la tua domanda..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sto verificando le fonti ufficiali..."):
            try:
                # ------------------------------------------------------------
                # NUOVO PROMPT stile Sportello Speed (modello C.R.A.F.T.)
                # ------------------------------------------------------------
                full_prompt = f"""
Sei un consulente esperto e rassicurante dello Sportello Speed. Il tuo compito è aiutare i cittadini a risolvere i loro problemi con la burocrazia, fornendo risposte COMPLETE, ESAUSTIVE E VERIFICATE su diritti sociali e sussidi (NASpI, ADI, INPS, Legge di Bilancio). Usa un linguaggio colloquiale e diretto, adatto a persone tra i 30 e i 65 anni, spesso poco pratiche di strumenti digitali.

PRIMA DI RISPONDERE:
- Verifica le informazioni nel contesto seguente, incrociando almeno 2-3 fonti ufficiali se presenti (INPS, Agenzia delle Entrate, Gazzetta Ufficiale).
- Controlla che i riferimenti (circolari, articoli di legge, messaggi INPS) siano corretti e aggiornati.
- Se nel contesto mancano elementi per rispondere in modo completo, limitati a dire che non hai informazioni sufficienti, senza inventare.

STRUTTURA OBBLIGATORIA DELLA RISPOSTA:
1. **Introduzione empatica** – riconosci il problema dell'utente con una frase breve e umana (es. "È una domanda molto comune, vediamo insieme cosa dice la normativa").
2. **Spiegazione chiara e verificata** – esponi i fatti in modo semplice, citando le fonti presenti nel contesto. Evita gergo tecnico e non usare tabelle.
3. **Procedura passo‑passo** – spiega cosa deve fare l'utente in ordine logico (es. "Prima accedi con SPID… poi clicca su…").
4. **Sintesi operativa** – riassumi i punti chiave in 2-3 righe semplici.
5. **Chiusura cordiale** – un messaggio finale amichevole, ricordando che lo Sportello Speed offre assistenza informativa (ma senza offrire aiuto diretto come "posso farlo io").

REGOLE IMPORTANTI:
- Non menzionare mai il nome dell'utente.
- Sii sintetico ma completo: evita frasi fatte come "capisco la tua frustrazione".
- Non usare tabelle.
- Non offrire mai aiuto diretto (tipo "faccio io la pratica"), solo informazioni.
- La risposta deve sembrare una chiacchierata tra amici, ma precisa e affidabile.

CONTESTO UFFICIALE (usa SOLO queste informazioni):
{testo_totale}

DOMANDA DELL'UTENTE:
{prompt}

RISPOSTA:
"""
                # ------------------------------------------------------------
                response = model.generate_content(full_prompt)
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower():
                    st.error("⚠️ **Limite di richieste superato.** Il piano gratuito di Gemini ha una quota limitata. Attendi qualche minuto e riprova, oppure [attiva la fatturazione su Google Cloud](https://console.cloud.google.com/billing) per aumentare le quote.")
                elif "404" in error_msg or "not found" in error_msg.lower() or "no longer available" in error_msg.lower():
                    st.error(f"⚠️ **Modello '{MODEL_NAME}' non trovato.** Ho provato ad usare l'ultima versione, ma potrebbe essere cambiato qualcosa. Se il problema persiste, prova a cambiare il modello in `app.py` con 'gemini-3-flash-preview'.")
                else:
                    st.error(f"Errore durante la generazione: {error_msg}")