def main(l):
    db = read_sequence("database.fa")
    index = {}

    # Store the indices of every lmer
    for j in range(len(db) - l + 1):
        lmer = db[j:j + l]
        if lmer in index:
            index[lmer].append(j)
        else: 
            index[lmer] = [j]

    # Output index for each l
    output_index(index, l)

def read_sequence(file):
    with open(file, "r") as f:
        return f.readlines()[1].strip()

def output_index(index, l):
    with open("results/index" + str(l) + ".txt", "w") as f:
        for lmer in sorted(index.keys()):
            positions = ",".join(map(str, index[lmer]))
            f.write(f"{lmer}\t{positions}\n")

if __name__ == "__main__":    
    for l in [3]:
        main(l)