import scripts.index_database as index_database
import scripts.exact_matches as exact_matches

def run_seed_and_extend(l, o, query_file, db_file):
    index_database.main(l, o, db_file)
    query = exact_matches.read_sequence(query_file)
    exact_matches.main(l, query, o)