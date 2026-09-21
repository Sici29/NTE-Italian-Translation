# Neverness to Everness (NTE) - Traduzione Italiana Completa

[![GitHub Release](https://img.shields.io/github/v/release/Sici29/NTE-Italian-Translation?color=blue&label=Versione)](https://github.com/Sici29/NTE-Italian-Translation/releases)
[![License: MIT](https://img.shields.io/badge/Licenza-MIT-green.svg)](LICENSE)
[![Buy Me A Coffee](https://img.shields.io/badge/Offrimi%20un%20caff%C3%A8-☕-orange.svg)](https://buymeacoffee.com/sici29)

Traduzione italiana amatoriale completa, professionale e pronta all'uso per **Neverness to Everness (NTE)**.

[☕ **Offrimi un caffè e sostieni le future traduzioni**](https://buymeacoffee.com/sici29)

Progetto sviluppato da **Sici29** e distribuito con installer automatico interattivo per Windows (Release **v1.0.0**).

---

## ✨ Caratteristiche della Traduzione

- **Copertura Totale (100%)**: Tutte le **100.848 voci** del gioco sono state interamente localizzate e revisionate in italiano con standard qualitativo AAA.
- **Interfaccia, HUD & Menu**: Menu principale, schermate di caricamento, pop-up di sistema, impostazioni audio/video e comandi completamente in italiano.
- **Storia Principale & Prologo**: Campagna principale doppiata testualmente con massima fedeltà narrativa e cinematografica.
- **Missioni Secondarie & Leggende**: Tutte le quest opzionali, le investigazioni urbane e le storie dei personaggi.
- **Dialoghi Ambientali & Vita di Città**: Tutti i fumetti di dialogo, i passanti di Hethereau, le stazioni radio e i messaggi dell'app *Bagel*.
- **Abilità, Combattimento & Lore**: Schede personaggio, alberi dei talenti, abilità speciali (*Arc*), equipaggiamento e armi.
- **Personalizzazione Veicoli**: Tuning, carrozzeria, parti meccaniche e livree completamente tradotte.
- **Tag Rich Text Preservati al 100%**: Piena compatibilità con tutti gli stili e colori di gioco (`<blue>`, `<Orange>`, `<Title>`, ecc.).
- **Architettura di Fallback Dinamico**: In caso di futuri aggiornamenti del gioco contenenti nuove stringhe non ancora tradotte, il motore carica automaticamente il testo inglese ufficiale per i contenuti nuovi, consentendoti di continuare a giocare in italiano per tutto il resto senza crash né blocchi.

---

## 📦 Installazione Rapida (Per i Giocatori)

### Metodo 1: Installer Automatico (Consigliato)
1. Scarica l'ultima versione del pacchetto dalla sezione [Releases](https://github.com/Sici29/NTE-Italian-Translation/releases).
2. Assicurati che il gioco sia chiuso.
3. Fai doppio clic su **`Installa_Traduzione_Italiana.bat`** (oppure avvia direttamente lo script `tools/nte_it_installer.py`).
4. L'installer rileverà automaticamente la cartella di installazione di Neverness to Everness nelle tue librerie Steam o percorsi personalizzati.
5. Seleziona **`[1] Installa / Aggiorna Traduzione Italiana`**.
6. Avvia **Neverness to Everness** e goditi il gioco in italiano!

### Metodo 2: Ripristino File Originali (Disinstallazione)
Se in qualsiasi momento desideri rimuovere la traduzione italiana e tornare al gioco completamente in lingua originale:
1. Fai doppio clic su **`Ripristina_Originale.bat`** (oppure avvia l'installer e premi **`[3]`**).
2. Il gioco tornerà immediatamente al suo stato vanilla originario.

---

## 🛠️ Architettura Tecnica & Modding Unreal Engine 5

In Neverness to Everness, la localizzazione italiana è strutturata per essere **pulita, non invasiva e totalmente reversibile**:

1. **Montaggio Patch via Pak ad Alta Priorità (`pakchunk999-Windows_999_P.pak`)**:
   - La traduzione viene iniettata tramite un file pacchetto autonomo posizionato nella cartella `Client/WindowsNoEditor/HT/Content/Paks/` (o `HT/Content/Paks/`).
   - Il suffisso `_999_P` istruisce Unreal Engine a sovrapporre i file della traduzione sopra i dati base del gioco, **senza toccare né modificare i file originali**.
2. **Fallback Dinamico per gli Aggiornamenti**:
   - Qualsiasi testo presente nel file di patch viene mostrato in italiano. Se gli sviluppatori rilasciano un aggiornamento contenente nuove stringhe inedite, il gioco utilizzerà il fallback nativo in lingua inglese per le sole righe nuove, evitando schermate nere, stringhe vuote o crash.
3. **Punteggiatura & Accenti Corretti**:
   - I testi includono font e caratteri italiani estesi reali (`è`, `é`, `à`, `ò`, `ù`, `ì`), mantenendo intatta la formattazione grafica.

---

## 📂 Struttura della Repository

```text
├── assets/                          # Risorse grafiche e icone
├── data/                            # Database di localizzazione
│   └── translation_master.tsv       # Tutte le 100.848 stringhe tradotte e verificate
├── docs/                            # Documentazione tecnica
│   ├── GLOSSARIO.md                 # Glossario ufficiale terminologico
│   └── QUALITY_AUDIT.md             # Report audit qualità e verifica tag
├── payload/                         # Pacchetto patch per il montaggio in gioco
│   └── pakchunk999-Windows_999_P.pak# File patch pronto per il deploy
├── tools/
│   └── nte_it_installer.py          # Codice sorgente completo dell'installer
├── Installa_Traduzione_Italiana.bat # Launcher rapido di installazione
├── Ripristina_Originale.bat         # Launcher rapido di disinstallazione
├── Verifica_Integrita.bat           # Launcher verifica file e diagnostica
├── CHANGELOG.md                     # Cronologia delle versioni
├── LICENSE                          # Licenza open-source MIT
└── README.md                        # Questa guida
```

---

## ☕ Crediti & Supporto

- **Traduzione Italiana & Sviluppo Installer**: **Sici29**
- **Repository Ufficiale**: [github.com/Sici29/NTE-Italian-Translation](https://github.com/Sici29/NTE-Italian-Translation)

Se apprezzi questo lavoro e vuoi sostenere il tempo impiegato per la traduzione e il mantenimento dei futuri aggiornamenti:

👉 [**Offrimi un caffè su Buy Me a Coffee**](https://buymeacoffee.com/sici29) ☕

---

## ⚖️ Nota Legale

Questo progetto è una localizzazione amatoriale non ufficiale creata dalla community per i videogiocatori italiani.
Tutti i diritti del gioco, dei marchi, dei personaggi e delle risorse originali appartengono a Hotta Studio e ai rispettivi detentori. Per utilizzare la traduzione è necessaria una copia legittima di **Neverness to Everness**.
