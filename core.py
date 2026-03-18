import requests
import psutil
import time
from datetime import datetime

def check_balances(addresses):
    if not addresses: return {}
    try:
        url = f"https://blockchain.info/balance?active={'|'.join(addresses)}"
        r = requests.get(url, timeout=20)
        return r.json() if r.status_code == 200 else {}
    except: return {}

def get_sys_status():
    try:
        batt = psutil.sensors_battery()
        if batt: return batt.percent, batt.power_plugged
    except: pass
    return 100, True

def tg_api(action, token, payload):
    url = f"https://api.telegram.org/bot{token}/{action}"
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.json()
    except: return None
