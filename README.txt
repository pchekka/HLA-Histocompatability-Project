Data Files:

1. allele_output.csv 
	
	Details the star allele calls for 32 biological samples. There are calls for both alleles for eight different HLA genes (A, B, C, DPA1, DPB1, DQA1, DQB1, DRB1). 

2. all_CDS.fasta

	Contains the coding sequence for each allele of each HLA gene for each biological sample in FASTA format. The FASTA headers are <sample>_<gene>_<allele>, where allele is either 1 or 2. 

3. all_gene.fasta

	Contains the full gene sequence (including introns and untranslated regions) for each allele of each HLA gene for each biological sample in FASTA format. The FASTA headers are <sample>_<gene>_<allele>, where allele is either 1 or 2.


This project takes HLA typing results (what alleles each sample has), along with the FASTA sequences for those alleles, and turns them into a standardized HML (Histoimmunogenetics Markup Language) file.

HML is simply an XML file format used in immunogenetics labs (e.g., to exchange HLA data).

The goal of the project is:

-Parse the input files
-Organize the data
-Build an HML XML document


Project Breakdown 

histocompatibilityProj/
│
├── main.py
├── parser.py
├── data_manager.py
├── models.py
├── hml_writer.py
├── metadata.py
├── validator.py
│
├── allele_output.csv      ← input #1: allele calls
├── all_CDS.fasta          ← input #2: coding sequences
├── all_gene.fasta         ← input #3: genomic sequences
├── metadata.json          ← input #4: experiment metadata
│
└── result.hml             ← the output


Here’s the simplest possible explanation of what the project is achieving:
 CSV + FASTA + Metadata
            ↓
       Parsers read the files
            ↓
     DataManager combines them
            ↓
      HMLWriter builds XML
            ↓
       Final HML output file


1.main.py

This is the main script you run.
It does NOT do any data processing itself. Instead, it orchestrates all the other classes:
What main.py does step-by-step:
Reads command-line arguments (input CSV, input FASTA files, metadata JSON, output filename).
Calls the AlleleCSVParser to read allele calls.
Calls the FastaParser twice:
	once for CDS sequences
	once for genomic sequences
Calls MetadataLoader to read metadata.json.
Sends everything to DataManager, which assembles the data into structured objects.
Uses HMLWriter to build the HML XML tree.
Saves the final .hml file.



2.parser.py

This file contains two parser classes:
AlleleCSVParser

This reads allele_output.csv, which looks like:

sample, HLA-A_1, HLA-A_2, HLA-B_1, HLA-B_2, ...
HG002, 01:01, 26:01, 35:08, 38:01, ...

What this parser outputs:

A nested dictionary:

{
  "HG002": {
     "HLA-A": ["HLA-A*01:01:01:01", "HLA-A*26:01:01:01"],
     "HLA-B": ["HLA-B*35:08:01:01", "HLA-B*38:01:01:01"],
     ...
  },
  ...
}


B. FastaParser

Reads FASTA files (all_CDS.fasta and all_gene.fasta).
Each FASTA header follows this pattern:

>HG002_HLA-A_1
SEQUENCE...


The parser splits the header into:
sample ID
gene name
allele number (1 or 2)



3. models.py

Contains the SampleGeneData class.
This object stores all information for one gene in one sample, including:
	alleles (from the CSV)
	CDS sequences (from FASTA)
	genomic sequences (from FASTA)


4. data_manager.py

This file is the middle-man of the whole program.

It takes:
allele calls, CDS sequences, and genomic sequences and creates a structure organized like this:

{
  "HG002": {
      "HLA-A": SampleGeneData(...),
      "HLA-B": SampleGeneData(...),
      ...
  },
  ...
}


5. metadata.py

Loads a JSON file containing experiment metadata:

{
  "lab": "Cornejo Lab & UCSC BME160",
  "analyst": "Your Name",
  "software_version": "1.0",
  "sequencing_platform": "Illumina MiSeq",
  "date": "2025-01-01",
  "reference_database": "IMGT/HLA 3.50.0"
}


6. validator.py
Wraps the xmlschema library so we can validate the final HML XML file using the official schema.



7. hml_writer.py

This is the file that actually creates the HML XML file.

What it does:
Creates the <hml> tag
Creates the <header> section from metadata
For each sample:
	Adds a <sample> element
	Adds <typing> blocks for each gene
	Adds <allele-assignment>
	with <allele> tags inside

Saves everything to a .hml file


result.hml --> This is the final product — an XML document in official HML format.

Example command:
python main.py \
  --alleles allele_output.csv \
  --cds all_CDS.fasta \
  --genomic all_gene.fasta \
  --metadata metadata.json \
  --output result.hml
