# 🛡️ IP Attribution Validator (DNS-Based)

A tool to **validate IP-domain attributions** using DNS-based methods like `dig` and `nslookup`. This is useful for analysts or researchers verifying whether a specific IP truly belongs to a domain, helping to classify attributions as **True Positive** or **False Positive**.

---

## ✨ Features

- ✅ DNS-based attribution validation
- 📁 Supports **TXT** and **CSV** input formats
- 🧠 Classifies results as **True Positive** or **False Positive**
- 🧹 Filters and outputs **only True Positives**
- ⚡ Full automation with a bash script
- 💾 Outputs saved to local files

---

## 📥 Input Format

Each line in your input file must be formatted like:

<IP> DNS-<domain>

css
Copy
Edit

### Example (`input.txt` or `input.csv`):

3.109.254.159 DNS-masterdataapi.nseindia.com
40.104.77.104 DNS-autodiscover.nseinvest.com
3.7.140.26 DNS-elink.nse.co.in

yaml
Copy
Edit

---

## 📂 Files in the Repository

| File                      | Description                                                      |
|---------------------------|------------------------------------------------------------------|
| `attribution_validator.py`   | Validates IP-domain pairs using DNS tools                         |
| `filter_true_positives.py`   | Filters only True Positives from the validator’s output            |
| `run_validator.sh`           | Bash script to automate the validation and filtering process       |
| `README.md`                  | This documentation file                                           |
| `requirements.txt`           | (Optional) External dependency list (empty by default)             |

---

## ⚙️ How It Works

### 1️⃣ Validate IP-Domain Attribution

```bash
python3 attribution_validator.py -t input.txt -o output.txt
# OR
python3 attribution_validator.py -c input.csv -o output.txt
The script:

Uses dig and nslookup to look up domain A records

Matches those IPs with your provided IP

Labels each entry as:

✅ True Positive — IP matches the domain’s DNS resolution

❌ False Positive — IP does not match the domain

2️⃣ Filter Only True Positives
bash
Copy
Edit
python3 filter_true_positives.py -i output.txt -o true_positives.txt
This helper script takes the validator’s output and extracts only lines labeled True Positive.

⚡ One-Click Full Workflow (Automated)
Use the provided run_validator.sh script to perform the full validation and filtering process:

bash
Copy
Edit
chmod +x run_validator.sh

./run_validator.sh -t input.txt
# OR
./run_validator.sh -c input.csv -o output.txt
This will:

Run the validator script

Save the output to a file

Filter and extract only the True Positives

Default output filenames:

Full results → output.txt

Filtered results → true_positives.txt

📤 Output Files
File Name	Description
output.txt	Complete results (True + False Positives)
true_positives.txt	Clean list of confirmed True Positives only

💡 Example Output
text
Copy
Edit
IP              Domain                                  Result
====================================================================
3.109.254.159   masterdataapi.nseindia.com             True Positive
13.232.122.185  masterdataapi.nseindia.com             True Positive
40.104.77.104   autodiscover.nseinvest.com             False Positive
Filtered output in true_positives.txt:

text
Copy
Edit
3.109.254.159   masterdataapi.nseindia.com             True Positive
13.232.122.185  masterdataapi.nseindia.com             True Positive
🔧 Requirements
This tool uses standard Unix networking tools:

dig

nslookup

Install with:

bash
Copy
Edit
# Debian/Ubuntu/Kali
sudo apt install dnsutils

# macOS
brew install bind
📦 Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/MacTavish-exe/ip-attribution-validator.git
cd ip-attribution-validator
