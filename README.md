# 🛡️ FakeBuster - IA per il contrasto alle Fake News

![FakeBuster Banner](https://via.placeholder.com/800x200.png?text=Fake+Buster+-+Intelligenza+Artificiale+contro+la+Disinformazione)

**FakeBuster** è una piattaforma sperimentale basata su architettura web che integra modelli avanzati di Intelligenza Artificiale (NLP e Deep Learning) e partecipazione umana per creare un ecosistema informativo affidabile. L'obiettivo principale è ridurre la diffusione di disinformazione bloccandone la pubblicazione alla radice tramite una validazione preventiva e automatizzata.

---

## 🚀 Panoramica del Progetto

Negli ultimi anni, la diffusione di fake news ha rappresentato una delle principali sfide della società digitale. FakeBuster nasce per superare le limitazioni del *fact-checking* manuale, offrendo:
- **Analisi in tempo reale:** Valutazione semantica in meno di 5 secondi contro i minuti/ore dei sistemi tradizionali.
- **Disponibilità 24/7:** Automazione completa integrata nel processo di sottomissione dei post.
- **Approccio ibrido:** Unione di classificazione automatica tramite modelli Transformer e revisione manuale (sistema di appelli e segnalazioni) gestita da moderatori umani.

---

## 🌟 Funzionalità Principali (Core Features)

La piattaforma supporta due modalità di interazione distinte, modellate su una solida architettura dei ruoli:

### 👤 Utente Base (Lettore / Autore)
- **Pubblicazione Contenuti:** Inserimento di articoli e ricezione di una valutazione immediata.
- **Storico e Appelli:** Consultazione delle proprie analisi e possibilità di richiedere una "revisione manuale" (Appello) se un contenuto legittimo viene bloccato dall'IA.
- **Segnalazioni:** Partecipazione attiva al mantenimento della piattaforma tramite la segnalazione di contenuti pubblici ritenuti non veritieri.

### 🕵️ Fact-Checker (Moderatore)
- **Dashboard Operativa:** Storico globale dei contenuti.
- **Gestione Appelli:** Approvazione o rigetto dei ricorsi degli utenti con conseguente modifica dello stato di pubblicazione.
- **Supervisione Segnalazioni:** Verifica dei report degli utenti e rimozione definitiva dei contenuti accertati come manipolati.

---

## 🧠 Motore di Intelligenza Artificiale (AI Service)

Il cuore del sistema non si basa su semplici algoritmi deterministici o di keyword-matching, ma utilizza il **Transfer Learning** su architetture all'avanguardia.

### Architettura: XLM-ROBERTa
FakeBuster utilizza `XLM-ROBERTa` (base), un modello Transformer pre-addestrato su 2.5TB di dati in oltre 100 lingue. Questo garantisce:
- **Multilinguismo Nativo:** Capacità di operare sin da subito su notizie italiane ed inglesi.
- **Self-Attention:** Il modello elabora l'intero contesto della frase, cogliendo incongruenze semantiche tra titoli sensazionalistici e corpo dell'articolo.

### Pipeline "Fail-Fast" e Filtraggio
1. **Filtro Anti-Spam (Gibberish Detection):** Prima dell'inferenza neurale (computazionalmente costosa), il sistema usa algoritmi euristici per scartare keysmashing o testi privi di struttura linguistica.
2. **Language Detection:** Verifica delle lingue supportate (`it`, `en`).
3. **Inferenza e Soglia di Sicurezza:** Il post riceve uno *Score* che rappresenta la probabilità che la notizia sia **VERA**. Viene utilizzata una soglia (*Threshold*) rigorosa impostata a **0.7 (70%)**.

### Performance & Metriche (Validation Set)
Il modello è stato sottoposto a Fine-Tuning utilizzando un subset bilanciato (1.000 campioni) derivato dal dataset *WELFake*. 
La politica di "Zero Tolerance" adottata ha prodotto i seguenti risultati:
- **Accuracy:** `97.50%`
- **Recall (sui falsi):** `1.0000` (Nessuna fake news ha superato il filtro).
- **Precision:** `0.9505` (Fail-Secure: tolleranza di un leggero *over-blocking* per garantire un feed pulito).

---

## 🏗️ Architettura Software (Pattern MVC)

L'applicazione Backend è sviluppata in **Python** utilizzando il micro-framework **Flask**, strutturata rigorosamente in base al design pattern Model-View-Controller:

* **📦 Model (Tier 3 - Dati & Persistenza):** Gestito tramite `SQLAlchemy` e `MySQL`. Le entità principali includono `Account` (Users & FactCheckers), `Post`, `Appello` e `Segnalazione`.
* **⚙️ Controller (Tier 2 - Logica di Business):** Implementato tramite Blueprints Flask, diviso in sottosistemi:
  - `gestione_utenza`: Autenticazione e profili.
  - `gestione_pubblicazioni`: Intercetta la sottomissione, chiama l'AI Service e gestisce lo stato (Pubblicato/Bloccato).
  - `gestione_appelli` & `gestione_segnalazioni`: Logica di moderazione asincrona.
* **🔌 Services (Logica Esterna):** Il pacchetto `ai_service.py` isola completamente l'infrastruttura di inferenza ML dal core gestionale, offrendo pattern Singleton per il caricamento del modello PyTorch.
* **🎨 View (Tier 1 - WebContent):** Template HTML renderizzati dinamicamente lato server usando **Jinja2**, con segregazione delle interfacce (Guest, User, FactChecker).

---

## 🛠️ Stack Tecnologico

- **Linguaggio:** Python 3.10+
- **Web Framework:** Flask, Jinja2
- **Database:** MySQL, SQLAlchemy (ORM)
- **Machine Learning / NLP:** PyTorch, HuggingFace Transformers, scikit-learn
- **Data Engineering:** Pandas, Regex

---

## ⚙️ Installazione e Sviluppo

1. **Clona il repository**
   ```bash
   git clone https://github.com/EmilianoDG5/IS-FIA-FAKE-BUSTER.git
   cd IS-FIA-FAKE-BUSTER
   ```

2. **Crea un ambiente virtuale (consigliato)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Su Windows: venv\Scripts ctivate
   ```

3. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura il Database**
   - Assicurati che un server MySQL sia in esecuzione.
   - Crea un database vuoto.
   - Modifica le credenziali nel file di configurazione (`config.py` o `.env`).

5. **Avvia il server**
   ```bash
   python run.py
   ```
   *L'applicazione sarà disponibile su `http://127.0.0.1:5000`*

---

## 👥 Autori
- **Bruno Santo** (Matricola: 0512116161)
- **Emiliano Di Giuseppe** (Matricola: 0512119155)

*Progetto realizzato per il corso di Ingegneria del Software - Università degli Studi di Salerno (Gennaio 2026).*
