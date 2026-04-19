def main(l, query, o):
    # Find all (i,j) exact matches
    matches = []
    indexMap = get_indices(l, o)
    for j in range(len(query) - l + 1):
        lmer = query[j:j + l]
        if lmer in indexMap:
            for k in indexMap[lmer]:
                matches.append((j,k))

    # Write match file
    with open("results/match_" + o + "_" + str(l) + ".txt", "w") as f:
        for x, y in matches:
            f.write(f"{x},{y}\n")

def read_sequence(file):
    with open(file, "r") as f:
        return f.readlines()[1].strip()

def get_indices(l, o):
    with open("results/index_" + o + "_" + str(l) + ".txt", "r") as f:
        lines = f.readlines()
    index = {}
    for line in lines:
        line = line.strip()
        s, i = line.split("\t")
        index[s] = list(int(n) for n in i.split(","))
    return index