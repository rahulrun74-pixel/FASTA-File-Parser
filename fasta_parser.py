from Bio import SeqIO


def calculate_gc_content(sequence):
    """Calculate GC content percentage of a DNA sequence."""
    sequence = str(sequence).upper()

    if len(sequence) == 0:
        return 0.0

    gc_count = sequence.count("G") + sequence.count("C")
    return (gc_count / len(sequence)) * 100


def parse_fasta(filename):
    """Parse FASTA file and extract ID, length and GC content."""

    for record in SeqIO.parse(filename, "fasta"):
        sequence = record.seq

        sequence_id = record.id
        sequence_length = len(sequence)
        gc_content = calculate_gc_content(sequence)

        print(f"ID: {sequence_id}")
        print(f"Length: {sequence_length} bp")
        print(f"GC Content: {gc_content:.2f}%")
        print("-" * 40)


if __name__ == "__main__":
    parse_fasta("data/sample.fasta")