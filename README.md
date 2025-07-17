# 🔥 Personal Firewall Using Python

A simple and professional **Personal Firewall** built using Python with:

* **CLI Mode** (Stylish terminal colors)
*  **Tkinter GUI Mode** (Dark-themed stylish GUI)
*  **REST API Mode** (Flask API with Dark Mode Health Page)
*  **Docker support** for API deployment
*  **Logging system** with `firewall_log.txt`

---

##  Project Structure

```
├── firewall.py          # CLI Firewall
├── gui_firewall.py      # GUI with Tkinter
├── api_firewall.py      # Flask API
├── rules.json           # Blocked IPs and Ports
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker setup
└── firewall_log.txt     # Auto-created log file
```

---

##  Quick Start

###  Install Requirements

```bash
pip install -r requirements.txt
```

###  Run CLI Mode

```bash
python firewall.py
```

###  Run GUI Mode

```bash
python gui_firewall.py
```

###  Run REST API Mode

```bash
python api_firewall.py
```

###  Docker (Optional for API)

```bash
docker build -t personal-firewall .
docker run -p 5000:5000 personal-firewall
```

---

##  API Endpoints

| Endpoint      | Method | Description                       |
| ------------- | ------ | --------------------------------- |
| `/health`     | GET    | Dark Mode Status Page             |
| `/rules`      | GET    | View all blocked IPs/Ports        |
| `/rules/ip`   | POST   | Block an IP (`{"ip": "1.1.1.1"}`) |
| `/rules/port` | POST   | Block a port (`{"port": 80}`)     |
| `/logs`       | GET    | View firewall logs                |

Example to block IP using `curl`:

```bash
curl -X POST http://127.0.0.1:5000/rules/ip -H "Content-Type: application/json" -d '{"ip": "8.8.8.8"}'
```

---

##  Features

*  Modern Stylish Terminal (Color-coded output)
*  Dark Mode Tkinter GUI
*  REST API with health page
*  Docker Support for API
*  Realtime Logging System



