#!/usr/bin/env python3
# Firefox Cookie Extractor
# Extracts cookies from a Firefox profile for a given domain and saves them to a text file
# Usage: python firefox-cookie-extractor.py [domain] [profile_name]

import os
import sqlite3
import shutil
import tempfile
import sys
import configparser

# 📁 Get Firefox base path
def get_firefox_base_path():
    if sys.platform.startswith("win"):
        return os.path.join(os.environ["APPDATA"], "Mozilla", "Firefox")
    elif sys.platform.startswith("darwin"):
        return os.path.expanduser("~/Library/Application Support/Firefox")
    else:
        return os.path.expanduser("~/.mozilla/firefox")

# 🔍 Find default profile name
def find_default_profile_name():
    base_path = get_firefox_base_path()
    ini_path = os.path.join(base_path, "profiles.ini")

    if not os.path.exists(ini_path):
        return None

    config = configparser.RawConfigParser()
    config.read(ini_path)

    for section in config.sections():
        if config.has_option(section, "Default") and config.get(section, "Default") == "1":
            return config.get(section, "Path")

    return None

# 📂 List available profiles
def list_profiles():
    base_path = get_firefox_base_path()
    ini_path = os.path.join(base_path, "profiles.ini")

    if not os.path.exists(ini_path):
        print("❌ profiles.ini not found.")
        return

    config = configparser.RawConfigParser()
    config.read(ini_path)

    print("📂 Available Firefox profiles:")
    for section in config.sections():
        if config.has_option(section, "Name") and config.has_option(section, "Path"):
            name = config.get(section, "Name")
            path = config.get(section, "Path")
            print(f"  - {name}: {path}")

# 🧠 Show help message
def print_help():
    print("""
🧠 Usage:
  python youtui-cookie.py [domain] [profile_name]

📦 Options:
  --list-profiles     Show all available Firefox profiles
  --help              Display this help message

🌐 Examples:
  python youtui-cookie.py youtube.com
  python youtui-cookie.py twitter.com mw5j28sq.default-release-139257892109
""")

# 🔧 USER CONFIGURATION
USER_DEFINED_PROFILE = ""

# 🧭 Handle special flags
if len(sys.argv) > 1:
    if sys.argv[1] == "--help":
        print_help()
        exit(0)
    elif sys.argv[1] == "--list-profiles":
        list_profiles()
        exit(0)

# 🌐 Get domain and optional profile name from arguments
target_domain = sys.argv[1] if len(sys.argv) > 1 else "youtube.com"
profile_name = sys.argv[2] if len(sys.argv) > 2 else USER_DEFINED_PROFILE or find_default_profile_name()

if not profile_name:
    print("❌ No Firefox profile specified or detected.")
    exit(1)

print(f"🔍 Using Firefox profile: {profile_name}")

# 🔍 Build full path to cookies.sqlite
base_path = get_firefox_base_path()
db_path = os.path.join(base_path, profile_name, "cookies.sqlite")

# 🧾 Output filename based on domain
domain_label = target_domain.replace(".", "-")
script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(script_dir, f"cookie-{domain_label}.txt")
os.makedirs(os.path.dirname(out_path), exist_ok=True)

# 🧪 Check if cookies.sqlite exists
if not os.path.exists(db_path):
    print(f"❌ cookies.sqlite not found at: {db_path}")
    exit(1)

# 📁 Create temporary folder
temp_dir = tempfile.mkdtemp()
temp_db_path = os.path.join(temp_dir, "cookies.sqlite")

# 📦 Copy database and auxiliary files
shutil.copy2(db_path, temp_db_path)
for suffix in ["-wal", "-shm"]:
    src = db_path + suffix
    dst = temp_db_path + suffix
    if os.path.exists(src):
        shutil.copy2(src, dst)

# 🍪 Extract cookies
conn = sqlite3.connect(f"file:{temp_db_path}?mode=ro", uri=True)
cursor = conn.cursor()
cursor.execute("""
    SELECT name, value FROM moz_cookies
    WHERE host LIKE ?
""", (f"%{target_domain}%",))
cookies = cursor.fetchall()
conn.close()
shutil.rmtree(temp_dir)

# 🧾 Save cookies to file
cookie_string = "; ".join([f"{name}={value}" for name, value in cookies])

# 🔢 Show total number of cookies
print(f"🔢 Total cookies found: {len(cookies)}")

if cookie_string:
    with open(out_path, "w") as f:
        f.write(cookie_string + "\n")
    print(f"✅ Cookies for {target_domain} saved to: {out_path}")
else:
    print(f"⚠️ No cookies found for {target_domain}.")
