import argparse
import csv
import socket
import subprocess

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

def parse_txt(file):
    entries = []
    with open(file, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                ip, attr = parts
                if attr.startswith("DNS-"):
                    entries.append((ip, attr))
    return entries

def parse_csv(file):
    entries = []
    with open(file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                ip, attr = row[0].strip(), row[1].strip()
                if attr.startswith("DNS-"):
                    entries.append((ip, attr))
    return entries

def validate_dns(ip, domain):
    dig_ips = run_dig(domain)
    ns_ips = run_nslookup(domain)
    all_ips = set(dig_ips + ns_ips)
    return ip in all_ips

def main():
    parser = argparse.ArgumentParser(description="DNS Attribution Validator")
    parser.add_argument("-t", help="Input text file")
    parser.add_argument("-c", help="Input CSV file")
    parser.add_argument("-o", help="Output file name")
    args = parser.parse_args()

    if not args.t and not args.c:
        print("Error: Please provide either -t <textfile> or -c <csvfile> as input.")
        return

    entries = []
    if args.t:
        entries = parse_txt(args.t)
    elif args.c:
        entries = parse_csv(args.c)

    results = []
    header = f"{'IP':<15}\t{'Domain':<40}\t{'Result'}"
    results.append(header)
    results.append("=" * len(header))

    for ip, attr in entries:
        domain = attr.replace("DNS-", "")
        valid = validate_dns(ip, domain)
        result = "True Positive" if valid else "False Positive"
        results.append(f"{ip:<15}\t{domain:<40}\t{result}")

    for line in results:
        print(line)

    if args.o:
        with open(args.o, "w") as f:
            f.write("\n".join(results))
        print(f"\nOutput written to {args.o}")

if __name__ == "__main__":
    main()
