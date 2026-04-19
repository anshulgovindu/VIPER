def main(l, o, db_file="database.fa"):
    db = read_sequence(db_file)
    index = {}

    # Store the indices of every lmer
    for j in range(len(db) - l + 1):
        lmer = db[j:j + l]
        if lmer in index:
            index[lmer].append(j)
        else: 
            index[lmer] = [j]

    # Output index for each l
    output_index(index, l, o)

def read_sequence(file):
    with open(file, "r") as f:
        return "".join(line.strip() for line in f.readlines() if not line.startswith(">"))

def output_index(index, l, o):
    with open("results/index_" + o + "_" + str(l) + ".txt", "w") as f:
        for lmer in sorted(index.keys()):
            positions = ",".join(map(str, index[lmer]))
            f.write(f"{lmer}\t{positions}\n")
