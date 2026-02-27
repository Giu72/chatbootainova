import streamlit as st
import google.generativeai as genai
from cervello import testo_totale
import time

# ---------------------------
# 1. Configurazione pagina
# ---------------------------
st.set_page_config(page_title="Ai-Nova 2026", page_icon="📂")
st.title("🎉 Ai-Nova: Assistente Diritti Sociali")
st.markdown("Chiedimi info su NASpI, ADI e Legge di Bilancio 2026.")

# ---------------------------
# 2. Configurazione AI con secrets
# ---------------------------
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("🔑 Chiave API non trovata. Crea il file `.streamlit/secrets.toml` con GOOGLE_API_KEY.")
    st.stop()

genai.configure(api_key=api_key, transport='rest')

# --- MODIFICA QUI: Aggiorna il modello all'ultima versione Flash ---
# Il vecchio modello 'gemini-2.0-flash-lite' non è più disponibile per i nuovi utenti.
# Utilizziamo il suo successore, 'gemini-2.5-flash', che mantiene costi e performance simili.
MODEL_NAME = 'gemini-2.5-flash'
# In alternativa, puoi provare l'ultima preview: 'gemini-3-flash-preview'
# MODEL_NAME = 'gemini-3-flash-preview'

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
        with st.spinner("Sto consultando i documenti..."):
            try:
                full_prompt = f"""
                Sei 'Ai-Nova', un assistente esperto in diritti sociali e sussidi (NASpI, ADI, INPS).
                USA SOLO IL CONTESTO SEGUENTE PER RISPONDERE.
                SE L'INFORMAZIONE NON C'È, DI': 'Non trovo informazioni ufficiali su questo punto'.

                CONTESTO UFFICIALE:
                {testo_totale}

                DOMANDA UTENTE:
                {prompt}

                RISPOSTA (Sii chiaro, empatico e cita la fonte se possibile):
                """
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