# Changelog - Neverness to Everness (NTE) Traduzione Italiana

Tutte le modifiche degne di nota a questo progetto saranno documentate in questo file.

---

## [1.4.0] - 2026-10-28

### Aggiunto & Aggiornato
- **Allineamento Patch Ufficiale 28/10/2026 (Build 26207100 - 113.044 stringhe totali)**:
  - Estrazione diretta dal nuovo template binario IoStore (game.locres) aggiornato a 186 namespace e 93.084 stringhe univoche (risolte tutte le voci mancanti).
  - Revisione e completamento integrale in italiano di oltre 4.600 stringhe residue (quest BlackBird, descrizioni abilità, dialoghi NPC e chat urbane).
  - Piena concordanza e verifica incrociata dinamica di genere maschile/femminile (<male=>...<male><female=>...<female>) con parallelo spagnolo e francese.
  - Chiusura universale conforme (</>) dei tag grafici e cromatici Unreal Engine.
  - Aggiornamento dell'installer autonomo alla versione **v1.4.0** con payload rigenerato.

---
## [1.3.0] - 2026-10-21

### Aggiunto & Aggiornato
- **Allineamento Patch Ufficiale 21/10/2026 (113.044 stringhe totali)**:
  - Traduzione completa dell'evento centenario "Celebrazione della Leggenda" (ST_Legend_Celebration).
  - Nuove missioni affinità e storie legate ad Akane Rin (ST_Likingquest_Akane).
  - Nuovi dialoghi ambientali, passanti e chat urbane.
  - Aggiornamento e ribilanciamento descrizioni abilità ed effetti di combattimento.
  - Normalizzazione ufficiale del nome del personaggio in **Akane Rin** (allineato alle versioni EN, ES e FR).
  - Piena gestione dei bivi di genere dinamico maschile/femminile (<male=>...<male><female=>...<female>) validati su parallelo spagnolo e francese.

---
## [1.0.0] - 2026-09-21

### Aggiunto
- **Traduzione Completa 100% (100.848 stringhe):**
  - Blocco 1: Interfaccia, HUD, Menu Principale, Impostazioni Audio/Video e Comandi.
  - Blocco 2: Oggetti, Inventario, Armi, Descrizioni del Mondo e Archivi.
  - Blocco 3: Prologo e Storia Principale (Main Quests).
  - Blocco 4: Missioni Secondarie, Storie delle Leggende e Missioni Mondiali.
  - Blocco 5: Dialoghi Ambientali, NPC, Vita di Città e Chat.
  - Blocco 6: Affinità Personaggi, Legami e Minigiochi (Mahjong, Biliardo, ecc.).
  - Blocco 7: Abilità Personaggi, Guide Tutorial, Negozi, Cucina e Personalizzazione Veicoli.
- **Installer Interattivo per Windows (CLI & Batch):**
  - Rilevamento automatico della cartella di gioco tramite registro e librerie Steam.
  - Funzione di installazione con sovrapposizione non distruttiva e backup automatico.
  - Ripristino pulito allo stato originale in un clic (disinstallazione completa).
  - Verifica di integrità crittografica e diagnostica.
  - Architettura di Fallback dinamico in inglese per future patch del gioco.
- **Documentazione:**
  - `GLOSSARIO.md`: Dizionario ufficiale della terminologia di gioco.
  - `QUALITY_AUDIT.md`: Resoconto dei controlli di qualità e validazione tag.
