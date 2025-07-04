import argparse
import csv
import subprocess
import re

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

def parse_input(file, mode):
    entries = []
    with open(file, "r") as f:
        if mode == "csv":
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    entries.append((row[0].strip(), row[1].strip()))
        else:
            for line in f:
                parts = line.strip().split(None, 1)
                if len(parts) == 2:
                    entries.append((parts[0].strip(), parts[1].strip()))
    return entries

def extract_domains(attribution_string):
    # Split on commas, strip spaces
    parts = [x.strip() for x in attribution_string.split(",")]
    dns_domains = []
    netblock_lines = []

    for part in parts:
        if re.search(r'Netblock|/\d{1,2}', part, re.IGNORECASE):
            netblock_lines.append(part)
        elif part.startswith("DNS-"):
            dns_domains.append(part.replace("DNS-", "").strip())
    return dns_domains, netblock_lines

def validate_ip_against_domains(ip, domains):
    for domain in domains:
        dig_ips = run_dig(domain)
        ns_ips = run_nslookup(domain)
        all_ips = set(dig_ips + ns_ips)
        if ip in all_ips:
            return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Advanced DNS Attribution Validator")
    parser.add_argument("-t", help="Input text file")
    parser.add_argument("-c", help="Input CSV file")
    parser.add_argument("-o", help="Output file name (default: output.txt)", default="output.txt")
    args = parser.parse_args()

    if not args.t and not args.c:
        print("Error: Please provide either -t <textfile> or -c <csvfile>")
        return

    entries = parse_input(args.t, "txt") if args.t else parse_input(args.c, "csv")

    results = []
    netblock_entries = []

    header = f"{'IP':<15}\t{'Domain(s)':<60}\t{'Result'}"
    results.append(header)
    results.append("=" * len(header))

    for ip, attr in entries:
        dns_domains, netblocks = extract_domains(attr)
        if netblocks:
            netblock_entries.append(f"{ip}\t{', '.join(netblocks)}")
            continue  # skip DNS validation for netblocks

        if dns_domains:
            valid = validate_ip_against_domains(ip, dns_domains)
            result = "True Positive" if valid else "False Positive"
            results.append(f"{ip:<15}\t{', '.join(dns_domains):<60}\t{result}")

    # Save DNS attribution results
    with open(args.o, "w") as f:
        f.write("\n".join(results))
    print(f"[+] DNS Validation results saved to: {args.o}")

    # Save netblock entries separately
    if netblock_entries:
        with open("netblocks.txt", "w") as f:
            f.write("\n".join(netblock_entries))
        print(f"[+] Netblock attributions saved to: netblocks.txt")

if __name__ == "__main__":
    main()
