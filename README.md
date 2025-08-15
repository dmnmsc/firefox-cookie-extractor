# 🦊 Firefox Cookie Extractor

Extract cookies from a Firefox profile for a given domain and save them to a text file (YouTube by default).

This tool is especially useful for extracting cookies from sites like `YouTube`, allowing `third-party applications` to authenticate or access content as if they were logged in via browser.

## 📦 Usage

```bash
python firefox-cookie-extractor.py [domain] [profile_name]
```
### Options

- `--help` — Show usage instructions  
- `--list-profiles` — List all available Firefox profiles

### Examples
```bash
python firefox-cookie-extractor.py github.com
python firefox-cookie-extractor.py twitter.com mw5j28sq.default-release-139257892109
```

## 📂 Output

Generates a file named `cookie-[domain]-com.txt` (e.g. `cookie-github-com.txt`) containing all cookies for the specified domain.

The cookies are saved in a single-line format, ready to be used in HTTP headers or tools like `curl`

## 🧠 Requirements

- Python 3
- Firefox installed with at least one user profile

## 🛠️ Features

- Automatically detects default Firefox profile  
- Supports manual profile selection  
- Works on Linux, macOS, and Windows  
- Temporary database copy to avoid file locks  
- Clean output with emoji-enhanced CLI messages 😎

## 👤 Author

Created by **dmnmsc**  
Feel free to fork, improve, or share!

## 📄 License

This project is licensed under the **GNU General Public License v3.0**.

You may freely use, modify, and distribute it under the terms of that license.

See the full license text here: [https://www.gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html)
