# Website Information Tool

A lightweight Python reconnaissance tool for gathering comprehensive website information including DNS records, WHOIS data, SSL certificates, and server details. Perfect for cybersecurity students and bug bounty hunters.

---

## Navigation
- [Features](#features)  
- [Installation](#installation)  
- [Usage](#usage)   
- [Author](#author)  
- [License](#license)  

---

## Features
- DNS enumeration (A, AAAA, MX, TXT, CNAME records)
- WHOIS domain information lookup
- SSL/TLS certificate details and expiry dates
- Server headers and technology stack detection
- JSON/CSV export for security reports
- CLI interface optimized for penetration testing workflows

---

## Installation
Clone the repository:  
```
git clone https://github.com/sujalkharatmol2732-crypto/Website-Information-Tool.git
```
Navigate to the project directory:  
```
cd Website-Information-Tool
```

Install required dependencies: 
```
pip install requests dnspython python-whois
```
Run the application:
```
python "Website Information Tool.py"
```
**Requirements:** 
---
Python 3.6+ with `requests`, `dnspython`, `python-whois` libraries.

---

## Usage
```
python "Website Information Tool.py" example.com
```

- Enter target domain when prompted
- View comprehensive reconnaissance results
- Export data to JSON/CSV format for reporting
- Ideal for subdomain enumeration prep and bug bounty recon

---

## Author
Sujal Kharatmol - Cybersecurity Student & Bug Bounty Hunter  
[LinkedIn](https://www.linkedin.com/in/sujal-kharatmol-2b5497397/) | [Medium](https://medium.com/@sujalkharatmol2732)

---

## License
MIT License - Feel free to use for educational and security research purposes.
