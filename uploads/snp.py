from Bio import SeqIO

def find_snps(seq1, seq2):
    snps = []
    for i, (base1, base2) in enumerate(zip(seq1, seq2)):
        if base1 != base2:
            snps.append((i + 1, base1, base2))  # 1-based index
    return snps

# Load sequences from a FASTA file (make sure the file has two sequences)
sequences = list(SeqIO.parse("example.fasta", "fasta"))

# Ensure we have exactly two sequences
if len(sequences) != 2:
    print("Please provide exactly two sequences for SNP comparison.")
else:
    seq1 = str(sequences[0].seq)
    seq2 = str(sequences[1].seq)

    # Truncate to the shorter length (if sequences are unequal)
    min_len = min(len(seq1), len(seq2))
    seq1 = seq1[:min_len]
    seq2 = seq2[:min_len]

    snps = find_snps(seq1, seq2)

    print("SNPs found at positions:")
    for pos, base1, base2 in snps:
        print(f"Position {pos}: {base1} -> {base2}")

