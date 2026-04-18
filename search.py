import argparse
import scripts.alignment.custom_alignment as custom_alignment
import scripts.alignment.biopython_alignment as biopy
import scripts.alignment.scikit_alignment as ska
from scripts.blastp_eval import alignment as bpa
import scripts.generate_hits as generate_hits
from scripts.mafft import mafft_local

def main(l):
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", type=argparse.FileType("r"), required=False, default='query.fa')
    parser.add_argument("-d", type=argparse.FileType("r"), required=False, default='database.fa')
    parser.add_argument("-m", type=int, required=False, default=1)
    parser.add_argument("-s", type=int, required=False, default=-2)
    parser.add_argument("-i", type=int, required=False, default=-2)
    parser.add_argument("-a", action="store_true", required=False, default='locAL')
    parser.add_argument("-b", action="store_true", required=False, default='BLOSUM62')
    parser.add_argument("-t", action="store_true", required=False, default=5)
    args = parser.parse_args()

    hits = generate_hits.main(l)
    output_alignments(hits, l, args)

def output_alignments(hits, l, args):
    q = get_sequence(args.q)
    db = get_sequence(args.d)
    with open("results/hits" + str(l) + ".txt", "w") as f:
        for i1, i2, j1, j2 in hits:
            
            # Run respective alignment
            if args.a == 'locAL':
                output = custom_alignment.local_alignment(args.m, args.s, args.i, q[i1:i2 + 1], db[j1:j2 + 1])
                
                # Offset indices: locAL shifts indices i1, j1 -> 0, 0
                output[0] += i1
                output[1] += i1
                output[2] += j1
                output[3] += j1

            elif args.a == 'biopy':
                output = biopy.align(q[i1:i2 + 1], db[j1:j2 + 1], args.b)

            elif args.a == 'ska':
                output = ska.align(q[i1:i2 + 1], db[j1:j2 + 1], args.b)
            
            elif args.a == 'mafft':
                mafft_local(q[i1:i2 + 1], "temp_query.fa")
                mafft_local(db[j1:j2 + 1], "temp_db.fa")

            # Write output if score >= threshold
            if output[4] >= args.t:
                f.write("\t".join(str(output[i]) for i in range(len(output))) + "\n")
                f.write(output[6] + "\n" + "|" * len(output[6]) + "\n" + output[7] + "\n\n")

            # Generate blast alignment file
            bpa(q[i1:i2 + 1], db[j1:j2 + 1])

def get_sequence(file):
    return file.readlines()[1].strip()

if __name__ == "__main__":
    for l in [3]:
        main(l)