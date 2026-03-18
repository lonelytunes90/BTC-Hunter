import argparse
from mnemonic import Mnemonic
from bitcoinlib.keys import Key
import config

def run_gen(count, words):
    mnemo = Mnemonic("english")
    strength = {12:128, 15:160, 18:192, 21:224, 24:256}.get(words, 128)
    
    print(f"[*] Generating {count} seeds and {count} keys...")
    with open(config.INPUT_FILE, "a", encoding="utf-8") as f:
        for _ in range(count):
            f.write(f"{mnemo.generate(strength=strength)}\n")
            f.write(f"{Key().wif()}\n")
    print(f"[+] Success. Added to {config.INPUT_FILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--words", type=int, default=12)
    args = parser.parse_args()
    run_gen(args.count, args.words)
