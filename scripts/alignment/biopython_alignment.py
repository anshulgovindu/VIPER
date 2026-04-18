# Implementing with BioPython
import math
from Bio.Align import substitution_matrices
from Bio import Align

def align(target, query, sub_matrix_name="BLOSUM62"):

    sub_matrix = substitution_matrices.load(sub_matrix_name)
    aligner = Align.PairwiseAligner(mode="local", substitution_matrix=sub_matrix)

    alignments = aligner.align(target, query)

    top_alignment = alignments[0]
    top_score = top_alignment.score
    e_value = e_val(top_score, len(query), len(target))

    return (top_score, top_alignment, e_value) # returns top score, top alignment, and e_value

def e_val(score, query_len, db_len, K=0.13, lam=0.318):

    search_space = query_len * db_len
    e_value = K * search_space * math.exp(-lam * score)

    return e_value

def test():
    target = "ITSVMFVHFCMRVVWMKQFESSGWPHEPDVSHNFCKIKWIKEMDLWDTHE"
    query = "SHDLNCLMCQFSPCIWPWHHMNSDYSEEPHNAHSPHCQFTFSTIHWLHGE"

    bit_score = align(target, query)[0]
    e_value = e_val(bit_score, len(query), len(target))
    print(e_value)