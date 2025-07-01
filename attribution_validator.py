import argparse
import csv
import socket
import ssl
import subprocess
import requests
from config import SHODAN_API_KEY, CENSYS_API_ID, CENSYS_API_SECRET

def run_dig(domain):
    try:
        output = subprocess.check_output(["dig", "+short", domain], text=True).strip().split("\n")
        return [ip for ip in output if ip and ip[0].isdigit()]
    except Exception:
        return []

def run_nslookup(domain):
    try:
        output = subprocess.check_output(["nslookup", domain], text=True)
        lines = output.split("\n")
        ips = []
        for line in lines:
            if "Address:" in line:
                parts = line.split(":")
                if len(parts) > 1 and parts[1].strip()[0].isdigit():
                    ips.append(parts[1].strip())
        return ips
    except Exception:
        return []

def check_ssl(ip):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((ip, 443), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=ip) as ssock:
                cert = ssock.getpeercert()
                return bool(cert)
    except Exception:
        return False

def check_open_port(ip, port=443):
    try:
        with socket.create_connection((ip, port), timeout=3):
            return True
    except Exception:
        return False

def shodan_lookup(ip):
    try:
        url = f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            return True
        return False
    except Exception:
        return False

def censys_lookup(ip):
    try:
        url = f"https://search.censys.io/api/v2/hosts/{ip}"
        response = requests.get(url, auth=(CENSYS_API_ID, CENSYS_API_SECRET))
        if response.status_code == 200:
            return True
        return False
    except Exception:
        return False

def parse_input(file=None, csv_mode=False):
    entries = []
    with open(file, "r") as f:
        if csv_mode:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    entries.append((row[0].strip(), row[1].strip()))
        else:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    entries.append((parts[0], parts[1]))
    return entries

def is_dns_based(attribution):
    return attribution.startswith("DNS-")

def validate_dns(ip, domain):
    dig_ips = run_dig(domain)
    ns_ips = run_nslookup(domain)
    all_ips = set(dig_ips + ns_ips)
    return ip in all_ips

def validate_keyword(ip):
    return check_open_port(ip) or check_ssl(ip) or shodan_lookup(ip) or censys_lookup(ip)

def main():
    parser = argparse.ArgumentParser(description="IP Attribution Validation Tool")
    parser.add_argument("file", help="Input file path (TXT or CSV)")
    parser.add_argument("-csv", action="store_true", help="Enable CSV mode")
    args = parser.parse_args()

    entries = parse_input(args.file, csv_mode=args.csv)

    print(f"{'IP':<15}\t{'Attribution':<40}\t{'Result'}")
    print("=" * 80)
    for ip, attr in entries:
        if is_dns_based(attr):
            domain = attr.replace("DNS-", "")
            valid = validate_dns(ip, domain)
            result = "True Positive (DNS)" if valid else "False Positive (DNS)"
        else:
            valid = validate_keyword(ip)
            result = "True Positive (Keyword)" if valid else "False Positive (Keyword)"
        print(f"{ip:<15}\t{attr:<40}\t{result}")

if __name__ == "__main__":
    main()
