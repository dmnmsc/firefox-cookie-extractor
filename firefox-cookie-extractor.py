#!/usr/bin/env python3
# Firefox and FirefoxPWA Cookie Extractor  + SOCS Filter
# Extracts cookies from a Firefox profile for a given domain and saves them to a text file

import os
import sqlite3
import shutil
import tempfile
import sys
import configparser
import json
import argparse

# 🔧 USER CONFIGURATION
USER_DEFINED_PROFILE = ""
FILTERED_COOKIES = {
    "youtube.com": ["SID", "HSID", "APISID", "SAPISID", "LOGIN_INFO", "YSC"],
    "google.com": ["HSID", "SSID", "APISID", "SAPISID", "SID", "LOGIN_INFO", "YSC"],
    "twitter.com": ["auth_token"]
}

# 📁 Get Firefox base path
def get_firefox_base_path():
    if sys.platform.startswith("win"):
        return os.path.join(os.environ["APPDATA"], "Mozilla", "Firefox")
    elif sys.platform.startswith("darwin"):
        return os.path.expanduser("~/Library/Application Support/Firefox")
    else:
        return os.path.expanduser("~/.mozilla/firefox")

# 📁 Get Firefox PWA base path
def get_firefox_pwa_path():
    if sys.platform.startswith("win"):
        return os.path.join(os.environ["LOCALAPPDATA"], "firefoxpwa", "profiles")
    elif sys.platform.startswith("darwin"):
        return os.path.expanduser("~/Library/Application Support/firefoxpwa/profiles")
    else:
        return os.path.expanduser("~/.local/share/firefoxpwa/profiles")

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
def list_profiles(use_pwa):
    base_path = get_firefox_pwa_path() if use_pwa else get_firefox_base_path()
    if use_pwa:
        print("📂 Available Firefox PWA profiles:")
        config_path = os.path.expanduser("~/.local/share/firefoxpwa/config.json")
        if not os.path.exists(config_path):
            print("❌ Firefox PWA config.json not found.")
            return
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                profiles = json.load(f).get("profiles", {})
        except Exception as e:
            print(f"❌ Failed to read config.json: {e}")
            return
        for ulid, profile_data in profiles.items():
            name = profile_data.get("name", ulid)
            print(f"  - {name}: {ulid}")
        return

    ini_path = os.path.join(base_path, "profiles.ini")
    if not os.path.exists(ini_path):
        print("❌ profiles.ini not found.")
        return
    config = configparser.RawConfigParser()
    config.read(ini_path)
    print("📂 Available Firefox profiles:")
    for section in config.sections():
        if config.has_option(section, "Name") and config.has_option(section, "Path"):
            print(f"  - {config.get(section, 'Name')}: {config.get(section, 'Path')}")

# 🔍 Resolve human-readable PWA profile name to ULID
def resolve_pwa_profile_name(name):
    config_path = os.path.expanduser("~/.local/share/firefoxpwa/config.json")
    if not os.path.exists(config_path):
        return None
    try:
        profiles = json.load(open(config_path, "r", encoding="utf-8")).get("profiles", {})
    except Exception:
        return None
    for ulid, profile_data in profiles.items():
        if profile_data.get("name", "").strip().lower() == name.strip().lower():
            return ulid
    return None

# 🌐 Validate domain format (basic check)
def is_valid_domain(domain):
    return "." in domain and not domain.endswith(".sqlite")

# 🧠 Argument parser
parser = argparse.ArgumentParser(
    description="Firefox and FirefoxPWA Cookie Extractor + SOCS Filter",
    formatter_class=argparse.RawTextHelpFormatter,
    epilog="""
📖 EXAMPLES:

  1️⃣ Extract cookies from YouTube using the default Firefox profile:
      python firefox-cookie-extractor.py youtube.com

  2️⃣ Extract cookies from Twitter using a specific standard profile:
      python firefox-cookie-extractor.py twitter.com myProfileName

  3️⃣ Extract cookies from Google using a PWA profile:
      python firefox-cookie-extractor.py google.com MyPWAProfile --pwa

  4️⃣ List all standard Firefox profiles:
      python firefox-cookie-extractor.py --list-profiles

  5️⃣ List all Firefox PWA profiles:
      python firefox-cookie-extractor.py --list-profiles --pwa

  6️⃣ Extract cookies from a PWA profile using its ULID:
      python firefox-cookie-extractor.py youtube.com 01HXXY9ZT8E6YQ5WZJ9NXYZ --pwa
"""
)

parser.add_argument("domain", nargs="?", default="youtube.com", help="Target domain (default: youtube.com)")
parser.add_argument("profile", nargs="?", default=None, help="Firefox profile name or ULID")
parser.add_argument("--pwa", action="store_true", help="Use Firefox PWA profile directory")
parser.add_argument("--list-profiles", action="store_true", help="List available profiles")
args = parser.parse_args()

# 📋 Handle profile listing
if args.list_profiles:
    list_profiles(args.pwa)
    sys.exit(0)

# 📋 Determine profile name
profile_name = args.profile or USER_DEFINED_PROFILE or find_default_profile_name()

# Swap if first arg looks like a profile name and not a domain
if args.pwa and not is_valid_domain(args.domain):
    print("⚠️ Domain argument seems to be a profile name. Swapping arguments.")
    profile_name, target_domain = args.domain, "youtube.com"
else:
    target_domain = args.domain

if not profile_name:
    print("❌ No Firefox profile specified or detected.")
    sys.exit(1)

if args.pwa:
    resolved = resolve_pwa_profile_name(profile_name)
    if resolved:
        profile_name = resolved

print(f"🔍 Using Firefox profile: {profile_name}")

# 🔍 Build full path to cookies.sqlite
base_path = get_firefox_pwa_path() if args.pwa else get_firefox_base_path()
db_path = os.path.join(base_path, profile_name, "cookies.sqlite")

# 🧪 Check if cookies.sqlite exists
if not os.path.exists(db_path):
    print(f"❌ cookies.sqlite not found at: {db_path}")
    sys.exit(1)

# 📁 Create temporary copy
temp_dir = tempfile.mkdtemp()
temp_db_path = os.path.join(temp_dir, "cookies.sqlite")
shutil.copy2(db_path, temp_db_path)
for suffix in ["-wal", "-shm"]:
    src = db_path + suffix
    if os.path.exists(src):
        shutil.copy2(src, temp_db_path + suffix)

# 🍪 Extract cookies
conn = sqlite3.connect(f"file:{temp_db_path}?mode=ro", uri=True)
cursor = conn.cursor()

if target_domain in FILTERED_COOKIES:
    filtered_names = FILTERED_COOKIES[target_domain]
    placeholders = ",".join("?" for _ in filtered_names)
    query = f"SELECT name, value FROM moz_cookies WHERE host LIKE ? AND name IN ({placeholders}) ORDER BY lastAccessed DESC"
    cursor.execute(query, (f"%{target_domain}", *filtered_names))
else:
    cursor.execute("SELECT name, value FROM moz_cookies WHERE host LIKE ?", (f"%{target_domain}",))

cookies = cursor.fetchall()
conn.close()
shutil.rmtree(temp_dir)

# 🧾 Save cookies to file
domain_label = target_domain.replace(".", "-")
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"cookie-{domain_label}.txt")
cookie_string = "; ".join([f"{name}={value}" for name, value in cookies])

print(f"🔢 Total cookies found: {len(cookies)}")

if cookie_string:
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cookie_string + "\n")
    print(f"✅ Cookies for {target_domain} saved to: {out_path}")
    print(f"\n✂️  {cookie_string}\n")
else:
    print(f"⚠️ No cookies found for {target_domain}.")
