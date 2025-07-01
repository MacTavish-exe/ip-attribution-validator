#!/bin/bash

# ---- Configurable defaults ----
INPUT_FILE=""
OUTPUT_FILE="output.txt"
TRUE_POSITIVES_FILE="true_positives.txt"
MODE=""

# ---- Help Menu ----
usage() {
    echo "Usage: $0 [-t text_file] [-c csv_file] [-o output_file]"
    echo
    echo "  -t    Input text file (with DNS-IP pairs)"
    echo "  -c    Input CSV file (with DNS-IP pairs)"
    echo "  -o    Output filename for DNS validator results (default: output.txt)"
    exit 1
}

# ---- Parse Arguments ----
while getopts "t:c:o:" opt; do
    case "$opt" in
        t) INPUT_FILE=$OPTARG; MODE="-t" ;;
        c) INPUT_FILE=$OPTARG; MODE="-c" ;;
        o) OUTPUT_FILE=$OPTARG ;;
        *) usage ;;
    esac
done

# ---- Validate input ----
if [[ -z "$INPUT_FILE" ]]; then
    echo "[!] Error: You must provide an input file using -t or -c"
    usage
fi

echo "[+] Running DNS Attribution Validator..."
python3 attribution_validator.py $MODE "$INPUT_FILE" -o "$OUTPUT_FILE"

echo "[+] Filtering True Positives..."
python3 filter_true_positives.py -i "$OUTPUT_FILE" -o "$TRUE_POSITIVES_FILE"

echo "[✓] Done. True Positives saved to $TRUE_POSITIVES_FILE"
