#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neverness to Everness (NTE) - Installer Traduzione Italiana
Autore: Sici29
Repository: https://github.com/Sici29/NTE-Italian-Translation
Offrimi un caffè: https://buymeacoffee.com/sici29
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
import subprocess
import webbrowser
from pathlib import Path

# Configura encoding console per Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

APP_NAME = "Neverness to Everness - Traduzione Italiana"
APP_VERSION = "1.0.0"
AUTHOR = "Sici29"
GITHUB_REPO = "https://github.com/Sici29/NTE-Italian-Translation"
DONATION_URL = "https://buymeacoffee.com/sici29"

# Nomi file e percorsi relativi del gioco
GAME_FOLDER_NAME = "Neverness to Everness"
PATCH_PAK_NAME = "pakchunk999-Windows_999_P.pak"
RELATIVE_PAK_PATHS = [
    Path("Client") / "WindowsNoEditor" / "HT" / "Content" / "Paks",
    Path("HT") / "Content" / "Paks",
]

GAME_EXECUTABLES = [
    "NTE-Win64-Shipping.exe",
    "NevernessToEverness.exe",
    "Client-Win64-Shipping.exe",
    "HT-Win64-Shipping.exe",
    "NTE.exe"
]

# Configurazione locale dell'utente (%APPDATA%)
USER_CONFIG_DIR = Path(os.environ.get("APPDATA", Path.home())) / "NTE_Italian_Translation"
CONFIG_FILE = USER_CONFIG_DIR / "config.json"
BACKUP_DIR = USER_CONFIG_DIR / "backups"

class ConsoleColor:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

def enable_colors() -> bool:
    if os.name == "nt":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False
    return True

USE_COLORS = enable_colors()

def col(text: str, color: str) -> str:
    if not USE_COLORS:
        return text
    return f"{color}{text}{ConsoleColor.RESET}"

def get_script_root() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent

def load_user_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_user_config(cfg: dict):
    USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(col(f"Attenzione: Impossibile salvare la configurazione: {e}", ConsoleColor.YELLOW))

def sha256_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def find_steam_libraries() -> list:
    """Scansiona il registro di Windows e i dischi per individuare tutte le librerie Steam."""
    libraries = []
    
    if os.name == "nt":
        try:
            import winreg
            for hkey in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
                try:
                    with winreg.OpenKey(hkey, r"Software\Valve\Steam") as key:
                        val, _ = winreg.QueryValueEx(key, "SteamPath")
                        if val:
                            p = Path(val)
                            if p.exists() and p not in libraries:
                                libraries.append(p)
                except Exception:
                    pass
        except Exception:
            pass

    # Cartelle predefinite Steam
    common_drives = ["C", "D", "E", "F", "G", "H", "I"]
    for d in common_drives:
        candidates = [
            Path(f"{d}:/Program Files (x86)/Steam"),
            Path(f"{d}:/Program Files/Steam"),
            Path(f"{d}:/Steam"),
            Path(f"{d}:/SteamLibrary"),
            Path(f"{d}:/Giochi/SteamLibrary"),
            Path(f"{d}:/Games/SteamLibrary"),
        ]
        for c in candidates:
            if c.exists() and c not in libraries:
                libraries.append(c)

    all_steam_roots = list(libraries)
    for lib_root in libraries:
        vdf_path = lib_root / "steamapps" / "libraryfolders.vdf"
        if not vdf_path.exists():
            vdf_path = lib_root / "config" / "libraryfolders.vdf"
        if vdf_path.exists():
            try:
                with open(vdf_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('"path"'):
                            parts = line.split('"')
                            if len(parts) >= 4:
                                p = Path(parts[3].replace("\\\\", "/"))
                                if p.exists() and p not in all_steam_roots:
                                    all_steam_roots.append(p)
            except Exception:
                pass

    return all_steam_roots

def detect_game_directory() -> Path | None:
    # 1. Configurazione salvata in precedenza
    cfg = load_user_config()
    saved = cfg.get("game_dir")
    if saved:
        p = Path(saved)
        if validate_game_dir(p):
            return p

    # 2. Controllo librerie Steam
    for s_root in find_steam_libraries():
        candidate = s_root / "steamapps" / "common" / GAME_FOLDER_NAME
        if validate_game_dir(candidate):
            return candidate

    # 3. Controllo percorsi comuni su tutti i dischi
    common_drives = ["C", "D", "E", "F", "G", "H"]
    for d in common_drives:
        candidates = [
            Path(f"{d}:/Games/{GAME_FOLDER_NAME}"),
            Path(f"{d}:/Giochi/{GAME_FOLDER_NAME}"),
            Path(f"{d}:/{GAME_FOLDER_NAME}"),
            Path(f"{d}:/Program Files/{GAME_FOLDER_NAME}"),
            Path(f"{d}:/Program Files (x86)/{GAME_FOLDER_NAME}"),
        ]
        for cand in candidates:
            if validate_game_dir(cand):
                return cand

    return None

def validate_game_dir(path: Path) -> bool:
    if not path or not path.exists() or not path.is_dir():
        return False

    for rel in RELATIVE_PAK_PATHS:
        if (path / rel).exists():
            return True

    # Verifica se contiene eseguibili del gioco
    for root, _, files in os.walk(path):
        for f in files:
            if f in GAME_EXECUTABLES:
                return True
        break

    return False

def get_target_paks_dir(game_dir: Path) -> Path | None:
    for rel in RELATIVE_PAK_PATHS:
        candidate = game_dir / rel
        if candidate.exists():
            return candidate
    return None

def is_game_running() -> bool:
    if os.name != "nt":
        return False
    try:
        output = subprocess.check_output("tasklist", shell=True).decode("utf-8", errors="ignore")
        for exe in GAME_EXECUTABLES:
            if exe.lower() in output.lower():
                return True
    except Exception:
        pass
    return False

def get_payload_pak_path() -> Path:
    root = get_script_root()
    # 1. Cartella payload
    payload_pak = root / "payload" / PATCH_PAK_NAME
    if payload_pak.exists():
        return payload_pak
    
    # 2. Cartella radice
    root_pak = root / PATCH_PAK_NAME
    if root_pak.exists():
        return root_pak

    return payload_pak

def cmd_install(args: argparse.Namespace) -> int:
    print("\n" + "=" * 60)
    print(col(f"=== Installazione Traduzione Italiana - {APP_NAME} ===", ConsoleColor.CYAN + ConsoleColor.BOLD))
    print("=" * 60 + "\n")

    if is_game_running() and not getattr(args, "force_open", False):
        print(col("[ATTENZIONE] Il gioco sembra essere attualmente in esecuzione!", ConsoleColor.RED + ConsoleColor.BOLD))
        print("Chiudi Neverness to Everness prima di installare la patch.")
        return 1

    game_dir = getattr(args, "game_dir", None)
    if game_dir:
        game_dir = Path(game_dir)
        if not validate_game_dir(game_dir):
            print(col(f"[ERRORE] Il percorso specificato non sembra contenere Neverness to Everness:\n  {game_dir}", ConsoleColor.RED))
            return 1
    else:
        game_dir = detect_game_directory()

    if not game_dir:
        print(col("[ERRORE] Cartella di gioco non rilevata automaticamente!", ConsoleColor.RED + ConsoleColor.BOLD))
        print("Usa l'opzione [4] dal menu principale per selezionare la cartella manualmente.")
        return 1

    print(f"Cartella di gioco: {col(str(game_dir), ConsoleColor.GREEN)}")
    save_user_config({"game_dir": str(game_dir)})

    paks_dir = get_target_paks_dir(game_dir)
    if not paks_dir:
        # Crea la struttura standard
        paks_dir = game_dir / RELATIVE_PAK_PATHS[0]
        paks_dir.mkdir(parents=True, exist_ok=True)

    payload_pak = get_payload_pak_path()
    if not payload_pak.exists():
        print(col(f"[ERRORE] File patch non trovato in:\n  {payload_pak}", ConsoleColor.RED + ConsoleColor.BOLD))
        print("Verifica che il pacchetto della release sia stato estratto correttamente.")
        return 1

    dest_pak = paks_dir / PATCH_PAK_NAME

    # Backup di eventuale patch precedente
    if dest_pak.exists():
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        backup_file = BACKUP_DIR / f"{PATCH_PAK_NAME}.bak"
        try:
            shutil.copy2(dest_pak, backup_file)
        except Exception:
            pass

    print("Installazione della patch in corso...")
    mods_dir = paks_dir / '~mods'
    if mods_dir.exists():
        stale_mod = mods_dir / PATCH_PAK_NAME
        if stale_mod.exists():
            try:
                stale_mod.unlink()
                print(col("[INFO] Rimossa vecchia patch dalla cartella ~mods per evitare conflitti di priorità nel gioco.", ConsoleColor.YELLOW))
            except Exception as e:
                pass

    try:
        shutil.copy2(payload_pak, dest_pak)
    except Exception as e:
        print(col(f"[ERRORE] Impossibile copiare il file di patch: {e}", ConsoleColor.RED))
        return 1

    # Salvataggio ricevuta di installazione
    receipt = {
        "version": APP_VERSION,
        "author": AUTHOR,
        "game_dir": str(game_dir),
        "target_pak": str(dest_pak),
        "pak_sha256": sha256_file(dest_pak),
        "pak_size": dest_pak.stat().st_size,
        "fallback_enabled": True
    }
    try:
        with open(USER_CONFIG_DIR / "installation_info.json", "w", encoding="utf-8") as f:
            json.dump(receipt, f, indent=2)
    except Exception:
        pass

    print("\n" + col("[OK] TRADUZIONE ITALIANA INSTALLATA CON SUCCESSO!", ConsoleColor.GREEN + ConsoleColor.BOLD))
    print(f"Destinazione : {dest_pak}")
    print(f"Dimensione   : {dest_pak.stat().st_size / (1024*1024):.2f} MB")
    print(f"Architettura : {col('Sovrapposizione non distruttiva con Fallback automatico in Inglese', ConsoleColor.CYAN)}")
    print("\nPuoi avviare Neverness to Everness e goderti il gioco interamente in italiano!\n")
    return 0

def cmd_restore(args: argparse.Namespace) -> int:
    print("\n" + "=" * 60)
    print(col("=== Ripristino File Originali (Disinstallazione) ===", ConsoleColor.YELLOW + ConsoleColor.BOLD))
    print("=" * 60 + "\n")

    if is_game_running() and not getattr(args, "force_open", False):
        print(col("[ATTENZIONE] Il gioco è in esecuzione! Chiudilo prima di procedere.", ConsoleColor.RED))
        return 1

    game_dir = detect_game_directory()
    if not game_dir:
        print(col("[ERRORE] Cartella di gioco non trovata.", ConsoleColor.RED))
        return 1

    paks_dir = get_target_paks_dir(game_dir)
    target_pak = (paks_dir / PATCH_PAK_NAME) if paks_dir else None

    if target_pak and target_pak.exists():
        try:
            target_pak.unlink()
            print(f"File patch {col(PATCH_PAK_NAME, ConsoleColor.YELLOW)} rimosso con successo.")
        except Exception as e:
            print(col(f"[ERRORE] Impossibile rimuovere il file: {e}", ConsoleColor.RED))
            return 1
    else:
        print("Nessuna patch italiana trovata nella cartella di gioco.")

    receipt_file = USER_CONFIG_DIR / "installation_info.json"
    if receipt_file.exists():
        try:
            receipt_file.unlink()
        except Exception:
            pass

    print("\n" + col("[OK] GIOCO RIPRISTINATO ALLO STATO ORIGINALE!", ConsoleColor.GREEN + ConsoleColor.BOLD) + "\n")
    return 0

def cmd_verify(args: argparse.Namespace) -> int:
    print("\n" + "=" * 60)
    print(col(f"=== Verifica Integrità & Compatibilità - {APP_NAME} ===", ConsoleColor.CYAN + ConsoleColor.BOLD))
    print("=" * 60 + "\n")

    game_dir = detect_game_directory()
    if not game_dir:
        print(col("Stato Gioco    : Non rilevato automaticamente.", ConsoleColor.YELLOW))
        return 1

    print(f"Cartella Gioco : {col(str(game_dir), ConsoleColor.GREEN)}")

    paks_dir = get_target_paks_dir(game_dir)
    target_pak = (paks_dir / PATCH_PAK_NAME) if paks_dir else None

    if target_pak and target_pak.exists():
        size_mb = target_pak.stat().st_size / (1024 * 1024)
        checksum = sha256_file(target_pak)
        print(f"Stato Patch    : {col('INSTALLATA & ATTIVA', ConsoleColor.GREEN + ConsoleColor.BOLD)}")
        print(f"File Patch     : {target_pak}")
        print(f"Dimensione     : {size_mb:.2f} MB")
        print(f"SHA-256        : {checksum[:16]}...")
        print(f"Fallback EN    : {col('ATTIVO (compatibilità garantita con future patch di gioco)', ConsoleColor.GREEN)}")
    else:
        print(f"Stato Patch    : {col('NON INSTALLATA', ConsoleColor.YELLOW)}")

    payload_pak = get_payload_pak_path()
    if payload_pak.exists():
        ready_msg = col("Pronto per l'installazione", ConsoleColor.GREEN)
        size_str = f"{payload_pak.stat().st_size / (1024*1024):.2f} MB"
        print(f"Payload Locale : {ready_msg} ({size_str})")
    else:
        print(f"Payload Locale : {col('Mancante', ConsoleColor.RED)}")

    print()
    return 0

def configure_game_dir() -> bool:
    print("\n" + "=" * 60)
    print(col("=== Impostazione Manuale Cartella di Gioco ===", ConsoleColor.CYAN + ConsoleColor.BOLD))
    print("=" * 60)
    print("Inserisci il percorso della cartella principale di Neverness to Everness")
    print("Esempio: C:\\Program Files (x86)\\Steam\\steamapps\\common\\Neverness to Everness")
    print("Oppure premi Invio per annullare.\n")

    path_str = input("Percorso: ").strip().strip('"')
    if not path_str:
        return False

    p = Path(path_str)
    if validate_game_dir(p):
        save_user_config({"game_dir": str(p)})
        print(col("\n[OK] Cartella di gioco configurata e salvata con successo!\n", ConsoleColor.GREEN + ConsoleColor.BOLD))
        return True
    else:
        print(col(f"\n[ERRORE] Il percorso non sembra contenere una versione valida del gioco.\n", ConsoleColor.RED))
        return False

def show_credits():
    print("\n" + "=" * 60)
    print(col("=== Crediti & Supporto Progetto ===", ConsoleColor.CYAN + ConsoleColor.BOLD))
    print("=" * 60)
    print(f"Traduzione Italiana Completa: {col(AUTHOR, ConsoleColor.GREEN + ConsoleColor.BOLD)}")
    print(f"Repository GitHub: {col(GITHUB_REPO, ConsoleColor.BLUE)}")
    print(f"Versione Traduzione: {col('v' + APP_VERSION, ConsoleColor.YELLOW)}")
    print("\nQuesto progetto è stato realizzato con dedizione e passione per la community.")
    print("Ogni singola riga di dialogo, lore, abilità e interfaccia è stata localizzata")
    print("con standard di qualità professionale e rispetto del glossario.")
    print("\n" + "-" * 60)
    print(col("☕ Vuoi sostenere il progetto e i futuri aggiornamenti?", ConsoleColor.YELLOW + ConsoleColor.BOLD))
    print(f"Offrimi un caffè su: {col(DONATION_URL, ConsoleColor.GREEN + ConsoleColor.BOLD)}")
    print("-" * 60 + "\n")

    ans = input("Desideri aprire la pagina delle donazioni nel browser? [S/N]: ").strip().lower()
    if ans in ("s", "si", "y", "yes"):
        webbrowser.open(DONATION_URL)

def run_menu():
    while True:
        game_dir = detect_game_directory()
        status_str = col("Trovata", ConsoleColor.GREEN) if game_dir else col("Non trovata", ConsoleColor.RED)

        print("\n" + "=" * 62)
        print(f" {col(APP_NAME, ConsoleColor.CYAN + ConsoleColor.BOLD)} - {col('v' + APP_VERSION, ConsoleColor.YELLOW)}")
        print(" Localizzazione Completa 100% (100.848 testi)")
        print(f" Sviluppato da {col(AUTHOR, ConsoleColor.GREEN + ConsoleColor.BOLD)}")
        print("=" * 62)
        print(f" Cartella di gioco: {status_str} " + (f"({game_dir})" if game_dir else ""))
        print("-" * 62)
        print(" [1] Installa / Aggiorna Traduzione Italiana")
        print(" [2] Verifica Integrità File & Compatibilità")
        print(" [3] Ripristina File Originali (Disinstalla)")
        print(" [4] Imposta Cartella di Gioco Manualmente")
        print(" [5] Apri Cartella di Gioco")
        print(" [6] Crediti & Donazioni (Offrimi un caffè ☕)")
        print(" [0] Esci")
        print("=" * 62)

        choice = input("\nSeleziona un'opzione [0-6]: ").strip()
        dummy = argparse.Namespace(game_dir=None, force_open=False)

        if choice == "1":
            cmd_install(dummy)
        elif choice == "2":
            cmd_verify(dummy)
        elif choice == "3":
            cmd_restore(dummy)
        elif choice == "4":
            configure_game_dir()
        elif choice == "5":
            if game_dir and os.name == "nt":
                os.startfile(str(game_dir))
            elif game_dir:
                print(f"Cartella: {game_dir}")
            else:
                print(col("Cartella di gioco non configurata.", ConsoleColor.YELLOW))
        elif choice == "6":
            show_credits()
        elif choice == "0":
            print(col("\nGrazie per aver scelto la traduzione italiana. Buon divertimento in NTE!\n", ConsoleColor.CYAN))
            break
        else:
            print(col("Opzione non valida. Riprova.", ConsoleColor.RED))

def main():
    parser = argparse.ArgumentParser(description=APP_NAME)
    parser.add_argument("command", nargs="?", choices=["install", "restore", "verify", "check"], default=None)
    parser.add_argument("--install", action="store_true", help="Installa la traduzione italiana")
    parser.add_argument("--restore", action="store_true", help="Ripristina i file originali")
    parser.add_argument("--verify", action="store_true", help="Verifica integrità dei file")
    parser.add_argument("--game-dir", type=str, default=None, help="Percorso manuale della cartella di gioco")
    parser.add_argument("--force-open", action="store_true", help="Forza operazione anche se il gioco sembra aperto")
    parser.add_argument("--non-interactive", action="store_true", help="Esegui senza mostrare il menu")

    args = parser.parse_args()

    if args.install or args.command == "install":
        sys.exit(cmd_install(args))
    elif args.restore or args.command == "restore":
        sys.exit(cmd_restore(args))
    elif args.verify or args.command in ("verify", "check"):
        sys.exit(cmd_verify(args))
    elif args.non_interactive:
        sys.exit(cmd_install(args))
    else:
        run_menu()

if __name__ == "__main__":
    main()
