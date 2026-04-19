# Viral Local Sequence Alignment Search Tool (VLAST)

A robust framework for performing sequence alignment between query COVID sequences and reference database (GISAID EpiCOV). Identifies potential hits and performs local alignments using multiple backend implementations. Returns all alignments with a higher score than threshold t.

## Features

- Multiple alignment backends: custom-built local alignment, Biopython, Scikit-bio
- Configurable scoring parameters (match, substitution, indel penalties)
- Threshold-based filtering for alignment results
- Automated hit generation and sequence parsing
- Support for BLOSUM62 and other scoring matrices

## Requirements

- Python 3.11+
- `numpy`, `biopython`, `scikit-bio` for additional alignment backends

## Installation

```bash
# Clone or download the repository
# Install optional dependencies (if needed)
pip install -r requirements.txt
```

## Project Structure

```
├── README.md                       # This file
├── database.fa                     # Example database FASTA file
├── query.fa                        # Example query FASTA file
├── data/                           # Input data files
│   └── spikeprot0723/             # Sample spike protein database
├── scripts/                        # Helper scripts
│   ├── search.py                  # Search interface
│   ├── alignment/                 # Alignment backend implementations
│   ├── index_database.py          # Database indexing
│   ├── generate_hits.py           # Hit generation
│   └── blastp_eval.py             # BLAST evaluation
└── results/                        # Output results directory

```

## Usage

### Basic Command

```bash
python search.py [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-o` | str | N/A | Output file name |
| `-q` | File | `query.fa` | Path to query FASTA file |
| `-d` | File | `database.fa` | Path to database FASTA file |
| `-l` | Int | `3` | L-mer length for seed-and-extend |
| `-m` | Int | `1` | Match score (reward for matching characters) |
| `-s` | Int | `-2` | Substitution penalty (mismatch penalty) |
| `-i` | Int | `-2` | Indel penalty (insertion/deletion penalty) |
| `-a` | String | `local` | Alignment backend: `local` (custom), `biopy` (Biopython), or `ska` (Scikit-bio) |
| `-b` | Flag | — | Use BLOSUM62 substitution matrix (for Biopython and Scikit-bio) |
| `-t` | Int | `5` | Score threshold (only output hits with score ≥ this value) |

### Example Usage

query.fa: sample query sequence in database.fa (expected to return exact match)
query2.fa: sample query sequence NOT in database.fa
database.fa: sample database (10 sequences) for testing purposes, which is much smaller than the complete GISAID one (~17 million sequences)
- the complete database is too large to upload to repository, and will needs to be extracted by the user (also for legal reasons)

```bash
# Default alignment with custom backend
python search.py -q query.fa -d database.fa

# Using Biopython with BLOSUM62 matrix and higher threshold
python search.py -q query.fa -d database.fa -a biopy -b -t 50

# Custom scoring parameters
python search.py -q query.fa -d database.fa -m 2 -s -3 -i -2 -t 100
```