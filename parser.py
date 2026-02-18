import csv
import re


def parse_allele_csv(path):
    """
    Returns:
    {
      "hg002": {
        "HLA-A": ["HLA-A*01:01", "HLA-A*26:01"],
        "HLA-B": [...]
      }
    }
    """
    result = {}

    with open(path, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            sample = row["sample"].strip().lower()
            result.setdefault(sample, {})

            for col, val in row.items():
                if not val or col == "sample":
                    continue

                match = re.match(r"(HLA-[A-Z0-9]+)_\d+", col)
                if not match:
                    continue

                gene = match.group(1)
                allele = val.strip()

                result[sample].setdefault(gene, []).append(allele)

    return result


def parse_fasta(path):
    """
    Generic FASTA parser.
    Returns:
    {
      "HLA-A": "ATGC...",
      "HLA-B": "ATGC..."
    }
    """
    result = {}
    current_gene = None
    seq_lines = []

    with open(path) as f:
        for line in f:
            line = line.strip()

            if line.startswith(">"):
                if current_gene:
                    result[current_gene] = "".join(seq_lines)

                header = line[1:]
                match = re.search(r"(HLA-[A-Z0-9]+)", header)
                if match:
                    current_gene = match.group(1)
                else:
                    current_gene = None

                seq_lines = []
            else:
                if current_gene:
                    seq_lines.append(line)

        if current_gene:
            result[current_gene] = "".join(seq_lines)

    return result

