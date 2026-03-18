# 🚀 BTC Hunter Toolkit 

A professional, multi-threaded Bitcoin wallet auditor optimized for **Termux (Android)**, **Linux**, and **Windows**. This toolkit automates the process of checking mnemonic seeds (BIP39/Electrum) and WIF keys for active balances.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## 🌟 Key Features
* **Multi-Standard Support:** Scans BIP39 (12-24 words), Electrum seeds, and WIF Private Keys.
* **Smart Derivation:** Checks Legacy (P2PKH), SegWit (P2SH), and Native SegWit (Bech32).
* **Telegram Remote Control:** * `/status` — Get live statistics (Scanned, Hits, BTC Found, Battery).
    * `/stop` — Safely shut down and save progress from your phone.
* **Auto-Updater:** Integrated `update.py` syncs with GitHub on every launch.
* **Power Guard:** Automatically saves and exits if device battery drops below 15%.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/lonelytunes90/BTC-Hunter.git
cd BTC-Hunter
```

2. Run the Installer
```bash
bash setup.sh
```
3. Activate the Environment
```bash
source venv/bin/activate
```

🚀 How to Use
Step 1: Configuration
Edit config.py with your Telegram BOT_TOKEN and CHAT_ID. Set ENABLE_TELEGRAM = True.

Step 2: Generate Audit List
```bash
python generator.py --count 100
```
Step 3: Start Scanning
```bash
python generator.py --count 100
```


📁 Project Structure
​main.py — Entry point and update manager.
​scanner.py — High-performance scanning engine.
​generator.py — Tool for bulk creating seeds and keys.
​core.py — API handlers and system logic.
​config.py — User-defined settings.
​update.py — GitHub synchronization logic.

​⚠️ Disclaimer
​Educational purposes only. This toolkit is intended for research and authorized wallet recovery. The author is not responsible for any misuse or illegal activity. Always handle private keys in a secure, offline environment.

​📄 License
​Distributed under the MIT License.
