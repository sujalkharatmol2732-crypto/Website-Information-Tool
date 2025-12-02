#!/usr/bin/env python3
"""
Recon-lite: Website Information Tool GUI Version
Uses Tkinter for a simple desktop app window.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import csv
import socket
import urllib.request
import urllib.error
from datetime import datetime
import threading

# --- Your Recon functions (same as CLI version) ---

def get_ip_address(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return "Not resolved"

def get_dns_records(domain, record_type):
    records = []
    try:
        if record_type == "A":
            records.append(get_ip_address(domain))
        elif record_type in ["MX", "NS"]:
            try:
                ai = socket.getaddrinfo(domain, None)
                for addr in ai:
                    records.append(f"{addr[4][0]} ({record_type})")
            except:
                pass
    except:
        pass
    return records if records else ["No records found"]

def get_whois_info(domain):
    try:
        whois_server = "whois.iana.org"
        query = f"{domain}\r\n"
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((whois_server, 43))
        sock.send(query.encode())
    
        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
        sock.close()
    
        return {
            "domain": domain,
            "whois_server": whois_server,
            "response_preview": response.decode('utf-8', errors='ignore')[:300] + "...",
            "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {"error": f"WHOIS failed: {str(e)}"}

def get_http_headers(domain):
    try:
        for protocol in ["https", "http"]:
            url = f"{protocol}://{domain}"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Recon-lite/1.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    info = dict(response.headers)
                    info["status_code"] = response.status
                    info["final_url"] = url
                    return info
            except urllib.error.URLError:
                continue
        return {"error": "Connection failed"}
    except Exception as e:
        return {"error": str(e)}

def save_to_json(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"JSON save failed: {e} - Website Information Tool:91")

def save_to_csv(data, filename):
    if not isinstance(data, dict) or not data:
        return
    try:
        flat_data = {k: str(v)[:100] if len(str(v)) > 100 else str(v) for k, v in data.items()}
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=flat_data.keys())
            writer.writeheader()
            writer.writerow(flat_data)
    except Exception as e:
        print(f"CSV save failed: {e} - Website Information Tool:103")

# --- GUI Application ---

class ReconLiteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recon-lite: Website Information Tool")
        self.root.geometry('800x600')
        
        self.label = tk.Label(root, text="Enter Domain:", font=("Arial", 14))
        self.label.pack(pady=5)
        
        self.domain_entry = tk.Entry(root, font=("Arial", 14), width=50)
        self.domain_entry.pack(pady=5)
        self.domain_entry.focus()
        
        self.scan_button = tk.Button(root, text="Scan", font=("Arial", 14), command=self.start_scan)
        self.scan_button.pack(pady=5)
        
        self.output_box = scrolledtext.ScrolledText(root, font=("Courier", 10), width=90, height=25)
        self.output_box.pack(pady=10)
    
    def start_scan(self):
        domain = self.domain_entry.get().strip().lower()
        if not domain:
            messagebox.showerror("Input Error", "Please enter a domain.")
            return
        if domain.startswith(('http://', 'https://')):
            domain = domain.split("://",1)[1]
        if domain.startswith("www."):
            domain = domain[4:]
        
        self.scan_button.config(state=tk.DISABLED)
        self.output_box.delete('1.0', tk.END)
        self.output_box.insert(tk.END, f"Scanning domain: {domain}\n\n")
        
        # Run the scan in a separate thread to keep UI responsive
        threading.Thread(target=self.run_scan, args=(domain,), daemon=True).start()
    
    def run_scan(self, domain):
        try:
            results = {
                "domain": domain,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ip_address": get_ip_address(domain),
                "a_records": get_dns_records(domain, "A"),
                "mx_records": get_dns_records(domain, "MX"),
                "ns_records": get_dns_records(domain, "NS"),
                "whois": get_whois_info(domain),
                "http_headers": get_http_headers(domain)
            }
            
            json_file = f"{domain}_recon.json"
            csv_file = f"{domain}_whois.csv"
            
            save_to_json(results, json_file)
            save_to_csv(results["whois"], csv_file)
            
            output_text = json.dumps(results, indent=2, ensure_ascii=False)
            
            self.output_box.insert(tk.END, output_text)
            self.output_box.insert(tk.END, f"\n\nScan complete!\n")
            self.output_box.insert(tk.END, f"Results saved to:\n  {json_file}\n  {csv_file}\n")
        except Exception as e:
            self.output_box.insert(tk.END, f"Error: {e}\n")
        finally:
            self.scan_button.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = ReconLiteApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
