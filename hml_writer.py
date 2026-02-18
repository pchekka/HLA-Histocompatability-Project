import xml.etree.ElementTree as ET


class HMLWriter:

    def __init__(self):
        self.namespace = "http://schemas.nmdp.org/spec/hml/1.0.1"

    def _format_sequence(self, seq, line_length=60):
        return "\n".join(
            seq[i:i + line_length]
            for i in range(0, len(seq), line_length)
        )

    def write(self, output_path, allele_dict, cds_dict, gene_dict):
        root = ET.Element(
            "hml",
            {
                "xmlns": self.namespace,
                "version": "1.0.1"
            }
        )

        for sample, genes in allele_dict.items():

            sample_elem = ET.SubElement(root, "sample", {"id": sample.upper()})


            for gene, alleles in genes.items():

                typing_elem = ET.SubElement(sample_elem, "typing", {"gene": gene})

                # ----- CDS consensus -----
                if gene in cds_dict:
                    cds_cons = ET.SubElement(typing_elem, "consensus-sequence")
                    cds_seq = ET.SubElement(cds_cons, "sequence")
                    cds_seq.text = "\n" + self._format_sequence(cds_dict[gene]) + "\n"

                # ----- FULL GENE consensus -----
                if gene in gene_dict:
                    gene_cons = ET.SubElement(typing_elem, "gene-consensus-sequence")
                    gene_seq = ET.SubElement(gene_cons, "sequence")
                    gene_seq.text = "\n" + self._format_sequence(gene_dict[gene]) + "\n"

                # ----- Allele assignment -----
                allele_assign = ET.SubElement(typing_elem, "allele-assignment")

                for allele in alleles:
                    ET.SubElement(allele_assign, "allele", {"name": allele})

        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(output_path, encoding="utf-8", xml_declaration=True)

