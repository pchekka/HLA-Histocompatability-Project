from parser import parse_allele_csv, parse_fasta
from hml_writer import HMLWriter


ALLELE_FILE = "allele_output.csv"
CDS_FILE = "all_CDS.fasta"
GENE_FILE = "all_gene.fasta"
OUTPUT_HML = "result.hml"


def main():

    print("Parsing allele CSV...")
    allele_dict = parse_allele_csv(ALLELE_FILE)

    print("Parsing CDS FASTA...")
    cds_dict = parse_fasta(CDS_FILE)

    print("Parsing full gene FASTA...")
    gene_dict = parse_fasta(GENE_FILE)

    print("Writing HML...")
    writer = HMLWriter()
    writer.write(
        OUTPUT_HML,
        allele_dict,
        cds_dict,
        gene_dict
    )

    print("Done.")


if __name__ == "__main__":
    main()
