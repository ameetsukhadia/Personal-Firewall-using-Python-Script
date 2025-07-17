import tkinter as tk, json, psutil, threading, time
from tkinter import messagebox, simpledialog, scrolledtext
from datetime import datetime

class FirewallGUI:
    def __init__(self, root):
        root.title("🚀 Stylish Personal Firewall")
        root.configure(bg="#1e1e1e")

        self.rules = self.load_rules()

        tk.Label(root, text="🚀 Personal Firewall GUI", font=("Arial", 20, "bold"), fg="cyan", bg="#1e1e1e").pack(pady=10)
        self.logs = scrolledtext.ScrolledText(root, height=15, width=80, bg="#2e2e2e", fg="lime", font=("Consolas", 12))
        self.logs.pack(pady=10)

        btn_frame = tk.Frame(root, bg="#1e1e1e")
        btn_frame.pack()

        tk.Button(btn_frame, text="Block IP", font=("Arial",12,"bold"), bg="red", fg="white", command=self.block_ip, width=15).grid(row=0,column=0,padx=10)
        tk.Button(btn_frame, text="Block Port", font=("Arial",12,"bold"), bg="orange", fg="white", command=self.block_port, width=15).grid(row=0,column=1,padx=10)

        self.refresh_logs()
        threading.Thread(target=self.monitor, daemon=True).start()

    def load_rules(self):
        try:
            with open('rules.json') as f: return json.load(f)
        except: return {"blocked_ips":[],"blocked_ports":[]}

    def save_rules(self): json.dump(self.rules, open('rules.json','w'), indent=4)
    def log_event(self,event): open('firewall_log.txt','a').write(f"{datetime.now()} - {event}\n"); self.refresh_logs()

    def refresh_logs(self):
        try:
            logs = open('firewall_log.txt').read()
            self.logs.delete(1.0, tk.END); self.logs.insert(tk.END, logs)
        except: self.logs.insert(tk.END, "\n🚀 No Logs Yet\n")

    def block_ip(self):
        ip = simpledialog.askstring("Block IP", "Enter IP to block:")
        if ip: self.rules['blocked_ips'].append(ip); self.save_rules(); messagebox.showinfo("Blocked", f"✅ Blocked IP: {ip}")

    def block_port(self):
        port = simpledialog.askinteger("Block Port", "Enter Port:")
        if port: self.rules['blocked_ports'].append(port); self.save_rules(); messagebox.showinfo("Blocked", f"✅ Blocked Port: {port}")

    def monitor(self):
        while True:
            for conn in psutil.net_connections(kind='inet'):
                if conn.raddr:
                    ip, port = conn.raddr.ip, conn.raddr.port
                    if ip in self.rules['blocked_ips'] or port in self.rules['blocked_ports']:
                        self.log_event(f"🚫 BLOCKED: {ip}:{port}")
            time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = FirewallGUI(root)
    root.mainloop()
