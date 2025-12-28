# FAKE BUSTER - AI Fact-Checking Agent

### Obiettivo del progetto
FakeBuster è un sistema intelligente basato su Deep Learning progettato per contrastare la disinformazione online. Utilizzando il modello di linguaggio **XLM-RoBERTa** addestrato sul dataset WELFake, il sistema analizza il contenuto semantico degli articoli di notizie per classificarli automaticamente come "Veri" o "Falsi" con un'accuratezza superiore al 98%.

---

### Membri del Team
* **Emiliano Di Giuseppe** (Matricola: 0512119155)
* **Bruno Santo** (Matricola: 0512116161)

---

### Cosa contiene questo repository
La struttura del progetto è organizzata come segue:

* **`/Training`**: Contiene gli script Python per il Data Engineering e il Machine Learning.
  * `check.py`: Script preliminare per verificare l'integrità del dataset e la correttezza delle colonne prima di iniziare.
  * `clean_data.py`: Script per la pulizia del dataset, rimozione bias (Reuters) e deduplicazione.
  * `train_network.py`: Script per il fine-tuning del modello XLM-RoBERTa e calcolo metriche.
* **`/app`**: Contiene il codice sorgente per l'integrazione del modello nel backend (API/Servizi).
* **`/docs`**: Contiene la documentazione tecnica, il report PDF e la presentazione del progetto.
* **`requirements.txt`**: Lista di tutte le librerie Python necessarie per eseguire il progetto.

---

### Istruzioni per l'installazione ed esecuzione

#### 1. Prerequisiti
Assicurati di avere Python installato (versione 3.9 o superiore).
Clona questo repository o scarica lo ZIP ed estrailo.

#### 2. Installazione delle dipendenze
Apri il terminale nella cartella principale del progetto ed esegui:

```bash
pip install -r requirements.txt