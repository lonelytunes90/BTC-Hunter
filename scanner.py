import os
import time
import threading
import logging
import queue
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from bitcoinlib.keys import HDKey
import config, core

logging.getLogger('bitcoinlib').setLevel(logging.ERROR)

class Hunter:
    def __init__(self):
        self.stats = {"checked": 0, "hits": 0, "btc": 0.0, "stop": False, "start": time.time()}
        self.msg_queue = queue.Queue()
        self.last_update_id = 0
        
        if config.ENABLE_TELEGRAM:
            threading.Thread(target=self._messenger, daemon=True).start()
            if config.REMOTE_CONTROL:
                threading.Thread(target=self._listener, daemon=True).start()

    def _messenger(self):
        last_report = time.time()
        while not self.stats["stop"]:
            try:
                msg = self.msg_queue.get(timeout=1)
                core.tg_api("sendMessage", config.BOT_TOKEN, {"chat_id": config.CHAT_ID, "text": msg, "parse_mode": "Markdown"})
                time.sleep(1.5)
            except queue.Empty: pass
            if time.time() - last_report > config.REPORT_INTERVAL:
                self.send_status("🕒 Hourly Update")
                last_report = time.time()

    def _listener(self):
        while not self.stats["stop"]:
            updates = core.tg_api("getUpdates", config.BOT_TOKEN, {"offset": self.last_update_id + 1})
            if updates and updates.get("ok"):
                for u in updates["result"]:
                    self.last_update_id = u["update_id"]
                    msg = u.get("message", {})
                    text = msg.get("text", "").lower()
                    if str(msg.get("chat", {}).get("id")) == config.CHAT_ID:
                        if text == "/status": self.send_status("📊 Manual Status")
                        elif text == "/stop":
                            self.stats["stop"] = True
                            self.msg_queue.put("🛑 Remote Stop Received.")
            time.sleep(5)

    def send_status(self, head):
        up = time.strftime("%H:%M:%S", time.gmtime(time.time() - self.stats["start"]))
        p, plug = core.get_sys_status()
        self.msg_queue.put(f"{head}\n🔎 Scanned: `{self.stats['checked']}`\n🍀 Hits: `{self.stats['hits']}`\n💰 Total: `{self.stats['btc']:.4f}`\n⏱ Uptime: `{up}`\n🔋 Battery: `{p}%`")

    def process(self, item):
        if self.stats["stop"]: return
        addrs, mapper = [], {}
        try:
            if len(item.split()) >= 12:
                seed = HDKey.from_passphrase(item)
                for gap, style in [(44, 'legacy'), (49, 'p2sh-segwit'), (84, 'segwit')]:
                    for i in range(config.DERIVATION_GAP):
                        c = seed.traverse(f"m/{gap}'/0'/0'/0/{i}")
                        a = c.address(witness_type=style); addrs.append(a)
                        mapper[a] = (c.wif(), item, f"BIP{gap}")
            else:
                pk = HDKey.from_wif(item); a = pk.address()
                addrs.append(a); mapper[a] = (item, "WIF", "Direct")

            for i in range(0, len(addrs), config.BATCH_SIZE):
                if self.stats["stop"]: break
                batch = addrs[i:i+config.BATCH_SIZE]
                res = core.check_balances(batch)
                for addr in batch:
                    bal = res.get(addr, {}).get("final_balance", 0)
                    if bal > 0:
                        self.stats["hits"] += 1
                        val = bal / 100_000_000
                        self.stats["btc"] += val
                        self.msg_queue.put(f"✅ WINNER: `{val} BTC`\nAddr: `{addr}`\nKey: `{mapper[addr][0]}`")
                        with open(config.HITS_FILE, "a") as f: f.write(f"{addr} | {val} | {mapper[addr][0]}\n")
            
            with open(config.HISTORY_FILE, "a") as f: f.write(item + "\n")
            self.stats["checked"] += 1
        except: pass

    def start(self):
        with open(config.INPUT_FILE, 'r') as f: all_keys = set(l.strip() for l in f if l.strip())
        done = set()
        if os.path.exists(config.HISTORY_FILE):
            with open(config.HISTORY_FILE, 'r') as f: done = set(l.strip() for l in f if l.strip())
        todo = list(all_keys - done)
        with ThreadPoolExecutor(max_workers=config.THREADS) as exe:
            pbar = tqdm(total=len(todo), desc="Hunting")
            for _ in exe.map(self.process, todo):
                if self.stats["stop"]: break
                pbar.update(1)
