#!/bin/bash

# --- Colors for Terminal ---
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}       BTC HUNTER TOOLKIT - VENV INSTALLER       ${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# 1. Detect Environment
if [ -d "$HOME/.termux" ]; then
    OS="Termux"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
else
    OS="Unknown"
fi

echo -e "[*] Detected System: ${YELLOW}$OS${NC}"

# 2. Install System Dependencies
echo -e "[*] Updating system packages..."
if [ "$OS" == "Termux" ]; then
    pkg update -y && pkg upgrade -y
    pkg install -y python clang make libcrypt libffi openssl git
elif [ "$OS" == "Linux" ]; then
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv python3-dev build-essential libssl-dev libffi-dev git
elif [ "$OS" == "macOS" ]; then
    if ! command -v brew &> /dev/null; then
        echo -e "${RED}[!] Homebrew not found.${NC}"
    else
        brew install python git
    fi
fi

# 3. Create and Activate Virtual Environment
echo -e "[*] Setting up Virtual Environment (${YELLOW}venv${NC})..."
python3 -m venv venv

# Activate venv (Detect shell type)
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# 4. Install Python Libraries inside venv
echo -e "[*] Installing Python dependencies into venv..."
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install bitcoinlib mnemonic tqdm requests psutil colorama
fi

# 5. Initialize Files
touch list.txt processed.log found.txt

# 6. Final Message
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ SETUP COMPLETE!${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "To start the hunter, use these commands:"
echo -e "${YELLOW}source venv/bin/activate${NC} (Linux/Mac/Termux)"
echo -e "${YELLOW}venv\Scripts\activate${NC} (Windows)"
echo -e "${CYAN}python generator.py --count 100${NC}"
echo -e "${CYAN}python main.py --threads 8${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
