import argparse

def filter_true_positives(input_file, output_file=None):
    with open(input_file, "r") as f:
        lines = f.readlines()

    filtered = []
    for line in lines:
        if "True Positive" in line and not line.strip().startswith("="):
            filtered.append(line)

    if output_file:
        with open(output_file, "w") as f:
            f.writelines(filtered)
        print(f"True positives written to {output_file}")
    else:
        print("".join(filtered))

def main():
    parser = argparse.ArgumentParser(description="Filter only True Positives from attribution results")
    parser.add_argument("-i", "--input", required=True, help="Input file from attribution validator")
    parser.add_argument("-o", "--output", help="Output file to save filtered true positives")
    args = parser.parse_args()

    filter_true_positives(args.input, args.output)

if __name__ == "__main__":
    main()
