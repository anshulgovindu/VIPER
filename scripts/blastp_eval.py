from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast import NCBIXML

# need to run alignment with target and query fasta files -- prints score, e-value, and alignment
def alignment(target_seq, query_seq):

    blastp_run = NcbiblastpCommandline(query=query_seq, subject=target_seq, outfmt=5, out = "pairwise_results.xml")

    stdout, stderr = blastp_run()

    with open("results/pairwise_results.xml", "r") as f:
        blast_records = NCBIXML.read(f)

    for alignment in blast_records.alignments:
        for hsp in alignment.hsps:
            print("Score:", hsp.score)
            print("E-value:", hsp.expect)
            print(hsp.query)
            print(hsp.match)
            print(hsp.sbjct)                    