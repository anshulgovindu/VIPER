# Viral Sequence Alignment Search Tool

A robust framework for performing sequence alignment between query COVID sequences and reference databases. Identifies potential hits and performs detailed local or global alignments using multiple backend implementations. Returns all alignments with a higher score than T.

## Features

- Multiple alignment backends: custom local alignment, Biopython, Scikit-bio, and MAFFT
- Configurable scoring parameters (match, substitution, indel penalties)
- Threshold-based filtering for alignment results
- Automated hit generation and sequence parsing
- Support for BLOSUM62 and other scoring matrices

## Requirements

- Python 3.11+
- Standard library (no required external dependencies for core functionality)
- Optional: `biopython`, `scikit-bio`, `mafft` for additional alignment backends

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
| `-m` | Int | `1` | Match score (reward for matching characters) |
| `-s` | Int | `-2` | Substitution penalty (mismatch penalty) |
| `-i` | Int | `-2` | Indel penalty (insertion/deletion penalty) |
| `-a` | String | `local` | Alignment backend: `local` (custom), `biopy` (Biopython), or `ska` (Scikit-bio) |
| `-b` | Flag | — | Use BLOSUM62 substitution matrix (for Biopython and Scikit-bio) |
| `-t` | Int | `5` | Score threshold (only output hits with score ≥ this value) |

### Examples

```bash
# Default alignment with custom backend
python search.py -q query.fa -d data/spikeprot0723/spikeprot0723.fasta

# Using Biopython with BLOSUM62 matrix and higher threshold
python search.py -q query.fa -d database.fa -a biopy -b -t 50

# Custom scoring parameters
python search.py -q query.fa -d database.fa -m 2 -s -3 -i -2 -t 100
```