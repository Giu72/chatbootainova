import google.generativeai as genai

# Configura la tua API KEY qui
genai.configure(api_key="AIzaSyDic62vIr0-PfFzrrG4-eHkACYDaV2tVS0")

# Inizializza il modello Gemini 1.5 Flash (Veloce e Free)
model = genai.GenerativeModel('gemini-1.5-flash')

def chiedi_ad_ainova(domanda_utente, contesto_documenti):
    prompt = f"""
    Sei 'Ai-Nova', un assistente esperto in diritti sociali e sussidi (NASpI, ADI, INPS).
    USA SOLO IL CONTESTO SEGUENTE PER RISPONDERE. 
    SE L'INFORMAZIONE NON C'È, DI': 'Non trovo informazioni ufficiali su questo punto'.
    
    CONTESTO UFFICIALE:
    {contesto_documenti}
    
    DOMANDA UTENTE:
    {domanda_utente}
    
    RISPOSTA (Sii chiaro, empatico e cita la fonte):
    """
    response = model.generate_content(prompt)
    return response.text