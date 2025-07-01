# IP Attribution Validator Tool

This tool helps validate whether an IP attribution to a domain is correct using DNS lookups, keyword-based checks, and threat intelligence APIs (Shodan & Censys).

---

## 🔧 Features

- Supports plain text or CSV input
- DNS-based validation using `dig` and `nslookup`
- Keyword-based validation via:
  - Port scans (80, 443)
  - SSL certificate checks
  - Shodan & Censys lookups

---

## 📥 Input Format

**Text Example:**
3.109.254.159	DNS-masterdataapi.nseindia.com
13.232.122.185	DNS-masterdataapi.nseindia.com
40.104.77.104	DNS-autodiscover.nseinvest.com
40.104.68.120	DNS-autodiscover.nseinvest.com

