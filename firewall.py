import psutil, time, json
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

BLOCK = Fore.RED + Style.BRIGHT
ALLOW = Fore.GREEN + Style.BRIGHT
INFO = Fore.CYAN + Style.BRIGHT

def load_rules():
    try:
        with open('rules.json') as f:
            return json.load(f)
    except:
        return {"blocked_ips": [], "blocked_ports": []}

def log_event(event):
    with open('firewall_log.txt', 'a') as f:
        f.write(f"{datetime.now()} - {event}\n")

def monitor_connections(rules):
    print(INFO + "🚨 Stylish CLI Firewall Started 🚨")
    while True:
        for conn in psutil.net_connections(kind='inet'):
            if conn.raddr:
                ip, port = conn.raddr.ip, conn.raddr.port
                if ip in rules['blocked_ips']:
                    print(BLOCK + f"🚫 BLOCKED IP: {ip}:{port}")
                    log_event(f"BLOCKED IP: {ip}:{port}")
                elif port in rules['blocked_ports']:
                    print(BLOCK + f"🚫 BLOCKED PORT: {ip}:{port}")
                    log_event(f"BLOCKED PORT: {ip}:{port}")
                else:
                    print(ALLOW + f"✅ Allowed: {ip}:{port}")
        time.sleep(1)

if __name__ == "__main__":
    try:
        monitor_connections(load_rules())
    except KeyboardInterrupt:
        print(INFO + "\n🟢 Firewall stopped by user.")
