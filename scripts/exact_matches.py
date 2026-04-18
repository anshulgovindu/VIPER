def main(l, query):
    # Find all (i,j) exact matches
    matches = []
    indexMap = get_indices(l)
    for j in range(len(query) - l + 1):
        lmer = query[j:j + l]
        if lmer in indexMap:
            for k in indexMap[lmer]:
                matches.append((j,k))

    # Write to csv file
    with open("results/match" + str(l) + ".csv", "w") as f:
        for x, y in matches:
            f.write(f"{x},{y}\n")

def read_sequence(file):
    with open(file, "r") as f:
        return f.readlines()[1].strip()

def get_indices(l):
    with open("results/index" + str(l) + ".txt", "r") as f:
        lines = f.readlines()
    index = {}
    for line in lines:
        line = line.strip()
        s, i = line.split("\t")
        index[s] = list(int(n) for n in i.split(","))
    return index

if __name__ == "__main__":
    query = read_sequence("query.fa")
    for l in [3]:
        main(l, query)