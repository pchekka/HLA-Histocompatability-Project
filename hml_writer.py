import xml.etree.ElementTree as ET


class HMLWriter:

    def __init__(self):
        self.namespace = "http://schemas.nmdp.org/spec/hml/1.0.1"

    def _format_sequence(self, seq, line_length=60):
        return "\n".join(
            seq[i:i + line_length]
            for i in range(0, len(seq), line_length)
        )

    def _input_with_default(self, prompt, default):
        """
        Prompt the user with a default. If they press Enter,
        the default is returned.
        """
        response = input(f"{prompt} [{default}]: ").strip()
        return response if response else default

    def write(self, output_path, allele_dict, cds_dict, gene_dict):

        root = ET.Element(
            "hml",
            {
                "xmlns": self.namespace,
                "version": "1.0.1"
            }
        )

        # ==================
        # HEADER WITH INPUT
        # ==================

        print("\n--- HML Header Info (press Enter to accept default) ---")

        lab = self._input_with_default(
            "Lab name", "Cornejo Lab"
        )

        analyst = self._input_with_default(
            "Analyst name", "Your Name"
        )

        software_version = self._input_with_default(
            "Software version", "1.0"
        )

        platform = self._input_with_default(
            "Sequencing platform", "Illumina MiSeq"
        )

        test_date = self._input_with_default(
            "Test date (YYYY-MM-DD)", "2025-12-05"
        )

        ref_db = self._input_with_default(
            "Reference database", "IMGT/HLA 3.52.0"
        )

        header = ET.SubElement(root, "header")
        ET.SubElement(header, "lab").text = lab
        ET.SubElement(header, "analyst").text = analyst
        ET.SubElement(header, "softwareVersion").text = software_version
        ET.SubElement(header, "sequencingPlatform").text = platform
        ET.SubElement(header, "testDate").text = test_date
        ET.SubElement(header, "referenceDatabase").text = ref_db

        # ================
        # SAMPLES / TYPING
        # ================

        for sample, genes in allele_dict.items():

            sample_elem = ET.SubElement(root, "sample", {"id": sample.upper()})

            for gene, alleles in genes.items():

                typing_elem = ET.SubElement(sample_elem, "typing", {"gene": gene})

                # ===== CDS consensus =====
                if gene in cds_dict:
                    cds_cons = ET.SubElement(typing_elem, "consensus-sequence")
                    cds_seq = ET.SubElement(cds_cons, "sequence")
                    cds_seq.text = "\n" + self._format_sequence(cds_dict[gene]) + "\n"

                # ===== Full gene sequence =====
                if gene in gene_dict:
                    gene_cons = ET.SubElement(typing_elem, "gene-consensus-sequence")
                    gene_seq = ET.SubElement(gene_cons, "sequence")
                    gene_seq.text = "\n" + self._format_sequence(gene_dict[gene]) + "\n"

                # ===== Allele assignment =====
                allele_assign = ET.SubElement(typing_elem, "allele-assignment")
                for allele in alleles:
                    ET.SubElement(allele_assign, "allele", {"name": allele})

        # ===============
        # WRITE OUTPUT
        # ===============

        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(output_path, encoding="utf-8", xml_declaration=True)

        print(f"\nHML written to: {output_path}\n")
