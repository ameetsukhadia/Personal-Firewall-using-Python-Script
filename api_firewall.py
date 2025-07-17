from flask import Flask, jsonify, request, make_response
import psutil, json, threading, time

app = Flask(__name__)

def load_rules():
    try: return json.load(open('rules.json'))
    except: return {"blocked_ips":[],"blocked_ports":[]}

def save_rules(r): json.dump(r, open('rules.json','w'), indent=4)
def log_event(e): open('firewall_log.txt','a').write(e+'\n')

@app.route('/health')
def health():
    return make_response("""
    <html style='background:#121212;color:#00FF7F;font-family:Arial;text-align:center;margin-top:100px'>
    <h1>🚀 Firewall API is Running!</h1><p>Dark Mode Status Page</p>
    </html>""", 200)

@app.route('/rules') 
def rules(): return jsonify(load_rules())

@app.route('/rules/ip', methods=['POST'])
def add_ip():
    ip = request.json.get('ip')
    if ip: rules = load_rules(); rules['blocked_ips'].append(ip); save_rules(rules); return jsonify(msg=f"Blocked IP {ip}"), 201
    return jsonify(error="Invalid IP"), 400

@app.route('/rules/port', methods=['POST'])
def add_port():
    port = request.json.get('port')
    if isinstance(port, int): rules = load_rules(); rules['blocked_ports'].append(port); save_rules(rules); return jsonify(msg=f"Blocked Port {port}"), 201
    return jsonify(error="Invalid Port"), 400

@app.route('/logs')
def logs():
    try: logs=open('firewall_log.txt').readlines()
    except: logs=[]
    return jsonify(logs=logs)

def monitor(): 
    while True:
        r = load_rules()
        for c in psutil.net_connections(kind='inet'):
            if c.raddr:
                ip, port = c.raddr.ip, c.raddr.port
                if ip in r['blocked_ips']: log_event(f"BLOCKED IP: {ip}:{port}")
                elif port in r['blocked_ports']: log_event(f"BLOCKED PORT: {ip}:{port}")
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=monitor, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
