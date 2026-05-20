# Advanced Port & Service Scanner + HTML Report
# Author: ChatGPT
# Educational Purpose Only

import socket
import threading
from datetime import datetime
import os

# Banner
print("=" * 60)
print("        ADVANCED PORT & SERVICE SCANNER")
print("=" * 60)

# User Input
target = input("Enter Target IP or Domain: ")
start_port = int(input("Enter Start Port: "))
end_port = int(input("Enter End Port: "))

# Resolve IP
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("[-] Invalid Target")
    exit()

print(f"\n[+] Target IP: {target_ip}")
print(f"[+] Scanning Ports {start_port} - {end_port}")
print(f"[+] Scan Started: {datetime.now()}\n")

open_ports = []
lock = threading.Lock()

# Scan Function
def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target_ip, port))

        if result == 0:

            # Get Service Name
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"

            # Banner Grabbing
            try:
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = sock.recv(1024).decode(errors="ignore").strip()
            except:
                banner = "No Banner"

            with lock:
                print(f"[OPEN] Port: {port} | Service: {service}")

                open_ports.append({
                    "port": port,
                    "service": service,
                    "banner": banner
                })

        sock.close()

    except:
        pass


# Multithreading
threads = []

for port in range(start_port, end_port + 1):
    thread = threading.Thread(target=scan_port, args=(port,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

# Scan End Time
scan_end = datetime.now()

# Create Reports Folder
if not os.path.exists("reports"):
    os.makedirs("reports")

# Report File Name
report_file = f"reports/scan_report_{target}.html"

# HTML Report
html_report = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Advanced Port Scan Report</title>

    <style>
        body {{
            font-family: Arial;
            background: #121212;
            color: white;
            padding: 20px;
        }}

        h1 {{
            color: #00ff99;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: #1e1e1e;
        }}

        th {{
            background: #00ff99;
            color: black;
            padding: 12px;
        }}

        td {{
            border: 1px solid #333;
            padding: 10px;
        }}

        tr:nth-child(even) {{
            background: #2b2b2b;
        }}

        .info {{
            margin-top: 10px;
            padding: 10px;
            background: #1e1e1e;
            border-left: 5px solid #00ff99;
        }}
    </style>

</head>

<body>

<h1>Advanced Port Scan Report</h1>

<div class="info">
    <p><strong>Target:</strong> {target}</p>
    <p><strong>Target IP:</strong> {target_ip}</p>
    <p><strong>Scan Started:</strong> {datetime.now()}</p>
    <p><strong>Total Open Ports:</strong> {len(open_ports)}</p>
</div>

<table>
    <tr>
        <th>Port</th>
        <th>Service</th>
        <th>Banner</th>
    </tr>
"""

# Add Data
for data in open_ports:
    html_report += f"""
    <tr>
        <td>{data['port']}</td>
        <td>{data['service']}</td>
        <td>{data['banner']}</td>
    </tr>
    """

html_report += """
</table>

</body>
</html>
"""

# Save Report
with open(report_file, "w", encoding="utf-8") as file:
    file.write(html_report)

# Final Output
print("\n" + "=" * 60)
print("[✓] SCAN COMPLETED")
print(f"[✓] Open Ports Found: {len(open_ports)}")
print(f"[✓] HTML Report Saved: {report_file}")
print("=" * 60)