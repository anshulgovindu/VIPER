import argparse
import scripts.alignment.default_alignment as default_alignment
import scripts.alignment.biopython_alignment as biopy
import scripts.alignment.affine_alignment as affine
import scripts.generate_hits as generate_hits
import scripts.run_seed_and_extend as seed_extend

def main():
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", type=str, required=True, help="Output file name")
    parser.add_argument("-q", type=argparse.FileType("r"), required=False, default='query.fa', help="Path to query file")
    parser.add_argument("-d", type=argparse.FileType("r"), required=False, default='database.fa', help="Path to database file")
    parser.add_argument("-l", type=int, required=False, default=3, help="L-mer length for seed-and-extend")
    parser.add_argument("-m", type=int, required=False, default=1, help="Match score, or gap-open score for affine alignment")
    parser.add_argument("-s", type=int, required=False, default=-2, help="Mismatch score, or gap-extend score for affine alignment")
    parser.add_argument("-i", type=int, required=False, default=-2, help="Indel score")
    parser.add_argument("-a", type=str, required=False, default='default', help="Alignment type: default (custom-built), biopy (Biopython), or affine (affine alignment)")
    parser.add_argument("-b", type=str, required=False, default='BLOSUM62', help="Specify substitution matrix (for biopy and affine). Uses BLOSUM62 by default")
    parser.add_argument("-t", type=int, required=False, default=5, help="Score threshold (only output hits with score ≥ this value)")
    args = parser.parse_args()
    
    seed_extend.run_seed_and_extend(args.l, args.o, args.q.name, args.d.name)
    hits = generate_hits.main(args.l, args.o)
    output_alignments(hits, args)

def output_alignments(hits, args):
    q_header, q_seq = get_sequence(args.q)
    db_header, db_seq = get_sequence(args.d)
    with open(f"results/{args.o}_{args.l}.txt", "w") as f:
        for i1, i2, j1, j2 in hits:
            
            # Run respective alignment
            if args.a == 'default':
                output = default_alignment.local_alignment(args.m, args.s, args.i, q_seq[i1:i2 + 1], db_seq[j1:j2 + 1])
                
                # Offset indices: locAL shifts indices i1, j1 -> 0, 0
                output[0] += i1
                output[1] += i1
                output[2] += j1
                output[3] += j1

                # Write output if score >= threshold
                if output[4] >= args.t:
                    f.write("\t".join(str(output[i]) for i in range(len(output))) + "\n")
                    f.write(q_header + "\n")
                    f.write(output[6] + "\n")
                    f.write("|" * len(output[6]) + "\n")
                    f.write(db_header + "\n")
                    f.write(output[7] + "\n\n")

            elif args.a == 'biopy':
                output = biopy.align(q_seq[i1:i2 + 1], db_seq[j1:j2 + 1], args.b)
                if output[0] >= args.t:
                    f.write(str(output[1]) + '\t' + str(output[0]) + "\n")

            elif args.a == 'affine':
                output = affine.affine_align(q_seq[i1:i2 + 1], db_seq[j1:j2 + 1], args.m, args.s, substitution_matrix=args.b)

def get_sequence(file):
    lines = file.readlines()
    header = lines[0].strip() if lines and lines[0].startswith(">") else ""
    sequence = "".join(line.strip() for line in lines if not line.startswith(">"))
    return header, sequence

if __name__ == "__main__":
    main()