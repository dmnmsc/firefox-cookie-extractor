# 📦 Changelog — Firefox Cookie Extractor v1.1

## 🆕 New Features

- **Domain-specific cookie filtering**  
  Introduced `FILTERED_COOKIES` dictionary to extract only relevant cookies per domain (e.g. YouTube, Google, Twitter).

- **FirefoxPWA support**  
  Added `--pwa` flag to extract cookies from [FirefoxPWA](https://github.com/filips123/FirefoxPWA) profiles.  
  Includes:
  - Custom profile path resolution
  - Reading `config.json` for profile metadata
  - Resolving human-readable profile names to ULIDs

- **Cookie ordering by last access**  
  Filtered cookies are now sorted by `lastAccessed DESC` to prioritize recent activity.

## 🛠 Improvements

- **Modular profile path handling**  
  Separated logic for standard Firefox and FirefoxPWA profile directories.

- **UTF-8 encoding for output files**  
  Ensures compatibility and proper formatting across systems.

- **Console output of cookie string**  
  Displays the extracted cookie string directly in the terminal for quick copy-paste.

- **Enhanced CLI help formatting**  
  Integrated `argparse` with `RawTextHelpFormatter` to keep indentation, spacing, and emojis in the help output.

- **Comprehensive usage examples in help output**  
  Added clearly formatted real-world examples covering default profile extraction, specific profiles, PWA profiles (by name or ULID), and profile listing.

## 🧠 CLI Enhancements

- **Updated help message**  
  Added documentation for the new `--pwa` flag and clarified usage examples.

- **Improved argument parsing**  
  More robust handling of flags and profile resolution.

## 🧹 Cleanup & Refactoring

- Reorganized function order for better readability
- Removed redundant logic in profile listing
- Maintained backward compatibility with version 1.0
