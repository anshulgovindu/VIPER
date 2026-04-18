import skbio
from skbio import Protein
from skbio.alignment import local_pairwise_align_protein

def sci_kit_align(file1, file2, gap_open_penalty=11, gap_extend_penalty=1, substitution_matrix=None):
    """
    Aligns two protein sequences with given penalties.

    Returns a tuple containing the alignment object, score, and start/end 
    positions for each sequence.
    """
    # Use 'next' because skbio.io.read returns a generator for FASTA files
    protein_one = next(skbio.io.read(file1, format='fasta', into=Protein))
    protein_two = next(skbio.io.read(file2, format='fasta', into=Protein))

    # Perform the alignment
    alignment = local_pairwise_align_protein(
        protein_one, 
        protein_two, 
        gap_open_penalty=gap_open_penalty, 
        gap_extend_penalty=gap_extend_penalty, 
        substitution_matrix=substitution_matrix
    )

    return alignment