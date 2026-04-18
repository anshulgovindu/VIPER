import scripts.index_database as index_database
import scripts.exact_matches as exact_matches

def run_seed_and_extend(l):
    index_database.main(l)
    query = exact_matches.read_sequence("query.fa")
    exact_matches.main(l, query)

run_seed_and_extend(3)