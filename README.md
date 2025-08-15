# 🦊 Firefox Cookie Extractor

Extract cookies from [Standard Firefox](https://www.firefox.com) or [FirefoxPWA](https://github.com/filips123/FirefoxPWA) profiles for a specific domain, and save them in a ready-to-use text file.

By default, it extracts `YouTube` cookies, and it supports **domain-specific filtering** for sites like `YouTube`, `Google`, and `Twitter`.

This tool is especially useful for integrating cookies into **third-party applications**, enabling them to authenticate or access content as if you were already logged into your browser.

---

## 📦 Usage

```bash
python firefox-cookie-extractor.py [domain] [profile_name_or_ULID] [options]
```
> 💡 **Quick tip:**  
> To extract YouTube cookies from your **default** Firefox profile, simply run:  
> ```bash
> python firefox-cookie-extractor.py
> ```


### Options

- `-h, --help` — Show usage instructions with examples  
- `--list-profiles` — List available profiles (standard by default; combine with `--pwa` for PWA)  
- `--pwa` — Use a **FirefoxPWA** profile directory

---
## 📋 Command Summary

| Command | Description | Notes |
|---------|-------------|-------|
| `python firefox-cookie-extractor.py` | Extract YouTube cookies from default Firefox profile | Default domain: `youtube.com` |
| `python firefox-cookie-extractor.py <domain>` | Extract cookies for a specific domain | Example: `github.com` |
| `python firefox-cookie-extractor.py <domain> <profile>` | Extract cookies from a specific profile | Example: `twitter.com myprofile.default-release` |
| `python firefox-cookie-extractor.py --list-profiles` | List standard Firefox profiles | Works without `<domain>` argument |
| `python firefox-cookie-extractor.py --list-profiles --pwa` | List FirefoxPWA profiles | Requires FirefoxPWA |
| `python firefox-cookie-extractor.py <domain> <profile> --pwa` | Extract cookies from a FirefoxPWA profile | Example: `google.com MyPWAProfile` |


---
## 📜 Examples

| # | Command | Description |
|---|---------|-------------|
| 1 | `python firefox-cookie-extractor.py` | Extract YouTube cookies from the default Firefox profile |
| 2 | `python firefox-cookie-extractor.py github.com` | Extract GitHub cookies from the default Firefox profile |
| 3 | `python firefox-cookie-extractor.py twitter.com myprofile.default-release` | Extract Twitter cookies from a specific Firefox profile |
| 4 | `python firefox-cookie-extractor.py --list-profiles` | List available standard Firefox profiles |
| 5 | `python firefox-cookie-extractor.py --list-profiles --pwa` | List available FirefoxPWA profiles |
| 6 | `python firefox-cookie-extractor.py google.com MyPWAProfile --pwa` | Extract Google cookies from a FirefoxPWA profile (by profile name) |
| 7 | `python firefox-cookie-extractor.py youtube.com 01H9YQ21CQZJX7WZJ0M5VY8R5T --pwa` | Extract YouTube cookies from a FirefoxPWA profile (by ULID) |


---

## 📂 Output

The script generates a file named:

```bash
cookie-[domain]-com.txt
```

For example:

```bash
cookie-github-com.txt
```

Cookies are saved in **a single-line format**, ready for direct use in HTTP headers or tools like:

```bash
curl --cookie "$(cat cookie-github-com.txt)" https://www.github.com
```

---

## 🧠 Requirements

- Python 3
- Firefox installed with at least one profile  
  *(or [FirefoxPWA](https://github.com/filips123/FirefoxPWA) if using `--pwa`)*
- Read access to the `cookies.sqlite` database

---

## 🛠️ Features

- **Domain-specific filtering** for cleaner cookie output
- Automatically detects the default profile
- Manual profile selection supported (name or ULID for PWA)
- Works on Linux, macOS, and Windows
- Temporary database copy to avoid file locks
- Clean, emoji-enhanced CLI output 😎
- Full support for [FirefoxPWA](https://github.com/filips123/FirefoxPWA)

---

## 🔒 Security note

The resulting cookie file contains **sensitive session data**. Store it securely and avoid sharing it. Rotate or delete cookies if compromised.

---

## 👤 Author

Created by **dmnmsc**  
Feel free to fork, improve, or share!

---

## 📄 License

This project is licensed under the **GNU General Public License v3.0**.  
You may freely use, modify, and distribute it under the terms of that license.

Full license text: [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.html)
