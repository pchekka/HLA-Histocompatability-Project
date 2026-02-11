import csv
import re


def parse_cds_fasta(path):
    """
    Parses CDS FASTA headers like:
    >THW09021_HLA-DRB1_1

    Returns:
    {
      "THW09021": {
        "HLA-DRB1": {
          "1": "ATG...",
          "2": "ATG..."
        }
      }
    }
    """
    cds = {}
    current_key = None
    current_seq = []

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith(">"):
                if current_key:
                    sample, gene, idx = current_key
                    cds.setdefault(sample, {}).setdefault(gene, {})[idx] = "".join(current_seq)

                header = line[1:]
                match = re.match(r"(.+?)_(HLA-[A-Z0-9]+)_(\d+)", header)
                if not match:
                    raise ValueError(f"Unexpected CDS header format: {header}")

                sample, gene, idx = match.groups()
                current_key = (sample, gene, idx)
                current_seq = []
            else:
                current_seq.append(line)

        if current_key:
            sample, gene, idx = current_key
            cds.setdefault(sample, {}).setdefault(gene, {})[idx] = "".join(current_seq)

    return cds

def parse_allele_csv(path):
    """
    Returns:
    {
      "THW09021": {
        "HLA-A": ["HLA-A*02:01", "HLA-A*24:02"],
        "HLA-DRB1": ["HLA-DRB1*04:01"]
      }
    }
    """
    result = {}

    with open(path, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            sample = row["sample"].strip()
            result.setdefault(sample, {})

            for col, val in row.items():
                if not val or val.strip() == "":
                    continue

                match = re.match(r"(HLA-[A-Z0-9]+)_\d+", col)
                if not match:
                    continue

                gene = match.group(1)
                allele = val.strip()

                result[sample].setdefault(gene, []).append(allele)

    return result
