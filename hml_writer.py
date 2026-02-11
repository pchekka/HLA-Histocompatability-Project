import xml.etree.ElementTree as ET
from xml.dom import minidom


def wrap_sequence(seq, line_length=60):
    return "\n".join(
        seq[i:i + line_length]
        for i in range(0, len(seq), line_length)
    )


class HMLWriter:
    def __init__(self, samples):
        self.samples = samples

    def write(self, output_path):

        # ---------- BUILD XML ----------
        hml = ET.Element(
            "hml",
            {
                "xmlns": "http://schemas.nmdp.org/spec/hml/1.0.1",
                "version": "1.0.1",
            },
        )

        for sample in self.samples:
            sample_el = ET.SubElement(hml, "sample", {"id": sample.sample_id})

            for typing in sample.typings:
                typing_el = ET.SubElement(sample_el, "typing", {"gene": typing.gene})

                if typing.consensus_sequence:
                    cs = ET.SubElement(typing_el, "consensus-sequence")
                    seq = ET.SubElement(cs, "sequence")
                    seq.text = "\n" + wrap_sequence(
                        typing.consensus_sequence.sequence
                    ) + "\n"

                aa = ET.SubElement(typing_el, "allele-assignment")
                for allele in typing.alleles:
                    ET.SubElement(aa, "allele", {"name": allele.name})

        # ---------- STRUCTURE PRETTY PRINT ----------
        rough_string = ET.tostring(hml, encoding="utf-8")
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")

        # Remove blank lines
        pretty_xml = "\n".join(
            line for line in pretty_xml.split("\n") if line.strip()
        )

        # ---------- FIX SEQUENCE INDENTATION ----------
        lines = pretty_xml.split("\n")
        fixed = []
        inside_sequence = False
        sequence_indent = ""

        for line in lines:
            stripped = line.lstrip()

            if stripped.startswith("<sequence>"):
                inside_sequence = True
                sequence_indent = line[:len(line) - len(stripped)]
                fixed.append(line)
                continue

            if stripped.startswith("</sequence>"):
                inside_sequence = False
                fixed.append(line)
                continue

            if inside_sequence:
                # indent relative to the <sequence> tag
                fixed.append(sequence_indent + "  " + stripped)
            else:
                fixed.append(line)

        final_xml = "\n".join(fixed)

        with open(output_path, "w") as f:
            f.write(final_xml)
