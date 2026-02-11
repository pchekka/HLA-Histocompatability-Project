#!/usr/bin/env python3
# Name: Pallavi Chekka (pchekka)
from models import Sample, Typing
from parser import parse_allele_csv, parse_cds_fasta
from hml_writer import HMLWriter


ALLELE_CSV = "allele_output.csv"
CDS_FASTA = "all_CDS.fasta"
OUTPUT_HML = "result.hml"


def main():
    allele_data = parse_allele_csv(ALLELE_CSV)
    cds_data = parse_cds_fasta(CDS_FASTA)

    samples = []

    for sample_id, genes in allele_data.items():
        sample = Sample(sample_id)

        for gene, alleles in genes.items():
            typing = Typing(gene)

            # allele assignment
            for allele in alleles:
                typing.add_allele(allele)

            # consensus sequence = CDS allele 1
            cds_seq = cds_data.get(sample_id, {}).get(gene, {}).get("1")
            if cds_seq:
                typing.set_consensus_sequence(cds_seq)

            sample.add_typing(typing)

        samples.append(sample)

    writer = HMLWriter(samples)
    writer.write(OUTPUT_HML)


if __name__ == "__main__":
    main()
