TOL = 1

def main(l, o):
    clusters = make_clusters(l, o)
    hits = clusters_to_hits(clusters)
    return hits
    
def make_clusters(l, o):
    pairs = get_indices(o, l)
    visited = set()
    clusters = []

    # Get single-linked clusters
    def dfs(pair):
        cluster = []
        stack = [pair]
        while stack:
            curr = stack.pop()
            if curr not in visited:
                visited.add(curr)
                cluster.append(curr)
                for i, j in pairs:
                    if (i, j) not in visited:
                        if abs(curr[0] - i) <= l + TOL and abs(curr[1] - j) <= l + TOL:
                            stack.append((i, j))
        return cluster

    for pair in pairs:
        if pair not in visited:
            cluster = dfs(pair)
            clusters.append(cluster)
    return clusters

def get_indices(o, l):
    with open("results/match_" + o + "_" + str(l) + ".txt", "r") as f:
        lines = f.readlines()
    pairs = []
    for line in lines:
        i, j = line.strip().split(",")
        pairs.append((int(i), int(j)))
    return pairs

def clusters_to_hits(clusters):
    hits = []
    for cluster in clusters:
        iMin = min(i for i, _ in cluster)
        iMax = max(i for i, _ in cluster)
        jMin = min(j for _, j in cluster)
        jMax = max(j for _, j in cluster)
        hits.append((iMin, iMax, jMin, jMax))
    return hits