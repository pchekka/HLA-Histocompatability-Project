class Allele:
    def __init__(self, name):
        self.name = name


class ConsensusSequence:
    def __init__(self, sequence):
        self.sequence = sequence


class Typing:
    def __init__(self, gene):
        self.gene = gene
        self.alleles = []
        self.consensus_sequence = None

    def add_allele(self, allele_name):
        self.alleles.append(Allele(allele_name))

    def set_consensus_sequence(self, sequence):
        self.consensus_sequence = ConsensusSequence(sequence)


class Sample:
    def __init__(self, sample_id):
        self.sample_id = sample_id
        self.typings = []

    def add_typing(self, typing):
        self.typings.append(typing)
