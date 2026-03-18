import subprocess, sys

def check_updates():
    print("[*] Checking GitHub...")
    try:
        subprocess.run(["git", "fetch"], check=True, capture_output=True)
        status = subprocess.run(["git", "status", "-uno"], capture_output=True, text=True).stdout
        if "behind" in status:
            print("[!] Update found. Pulling...")
            subprocess.run(["git", "pull"], check=True)
            print("[+] Updated. Please restart."); sys.exit(0)
    except: print("[-] Update check skipped (not a git repo).")
