import update, config, os
from scanner import Hunter

def main():
    print("--- BTC HUNTER TOOLKIT ---")
    if os.path.exists(".git"): update.check_updates()
    if not os.path.exists(config.INPUT_FILE):
        open(config.INPUT_FILE, "w").close()
        print(f"Created {config.INPUT_FILE}. Add seeds and restart.")
        return
    Hunter().start()

if __name__ == "__main__":
    main()
