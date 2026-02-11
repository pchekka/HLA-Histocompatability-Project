"""
data_manager.py
----------------
This class combines all parsed data into objects
that the HML writer can consume cleanly.

This is basically the "bridge" between parsing and writing.
"""

from models import SampleGeneData
from collections import defaultdict

class DataManager:
    """
    Combines allele CSV data + CDS fasta + genomic fasta into
    structured SampleGeneData objects.
    """

    def __init__(self, allele_dict, cds_dict, genomic_dict):
        self.allele_dict = allele_dict
        self.cds_dict = cds_dict
        self.genomic_dict = genomic_dict
        self.samples = defaultdict(dict)

    def assemble(self):
        """
        Creates a structure:

        self.samples = {
            sampleID: {
                gene: SampleGeneData(...)
            }
        }
        """

        for sample in self.allele_dict:
            for gene in self.allele_dict[sample]:
                # get the relevant CDS & genomic data (or empty dicts)
                cds_data = self.cds_dict.get(sample, {}).get(gene, {}) # Pull the CDS sequence block for this sample/gene
                gen_data = self.genomic_dict.get(sample, {}).get(gene, {}) # Pull the genomic sequence block for this sample/gene
                alleles = self.allele_dict[sample][gene]   # Pull allele calls for this sample/gene

                 # Create a SampleGeneData object 
                self.samples[sample][gene] = SampleGeneData(
                    alleles=alleles,
                    cds_dict=cds_data,
                    genomic_dict=gen_data
                )

        return self.samples
