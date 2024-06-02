import argparse
import pymysql
import json
import gzip
from tqdm import tqdm
import os  # Import os module for file path operations

# Get the directory of the current script file
script_dir = os.path.dirname(os.path.realpath(__file__))
# Construct the path to the db_config.json file
config_path = os.path.join(script_dir, 'db_config.json')

# Load database configuration
with open(config_path) as config_file:
    db_config = json.load(config_file)

fetch_options = {
    "gene_stable_id": {"text": "Gene Stable ID", "number": 1},
    "transcript_stable_id": {"text": "Ensembl Transcript ID", "number": 2},
    "protein_stable_id": {"text": "Ensembl Protein ID", "number": 3},
    "hgnc_id": {"text": "HGNC ID", "number": 4},
    "symbol": {"text": "Gene Symbol", "number": 5},
    "name": {"text": "Gene Description", "number": 6},
    "locus_group": {"text": "Locus Group", "number": 7},
    "locus_type": {"text": "Locus Type", "number": 8},
    "status": {"text": "Status", "number": 9},
    "location": {"text": "Chromosome Location", "number": 10},
    "location_sortable": {"text": "Chr loci sortable", "number": 11},
    "alias_symbol": {"text": "Gene Aliases", "number": 12},
    "alias_name": {"text": "Gene Description Aliases", "number": 13},
    "prev_symbol": {"text": "Previous Symbol", "number": 14},
    "prev_name": {"text": "Previous Name", "number": 15},
    "gene_group": {"text": "Gene Group", "number": 16},
    "gene_group_id": {"text": "Gene Group ID", "number": 17},
    "entrez_id": {"text": "Entrez Gene ID", "number": 18},
    "ensembl_gene_id": {"text": "Ensembl Gene ID", "number": 19},
    "vega_id": {"text": "VEGA ID", "number": 20},
    "ucsc_id": {"text": "UCSC ID", "number": 21},
    "ena": {"text": "ENA", "number": 22},
    "refseq_accession": {"text": "Refseq Accession", "number": 23},
    "uniprot_ids": {"text": "Uniprot ID", "number": 25},
    "pubmed_id": {"text": "Pubmed ID", "number": 26},
    "rgd_id": {"text": "RGD ID", "number": 28},
    "cosmic": {"text": "COSMIC Entry", "number": 30},
    "omim_id": {"text": "OMIM ID", "number": 31},
    "mirbase": {"text": "mirBase ID", "number": 32},
    "homeodb": {"text": "HomeoDB ID", "number": 33},
    "snornabase": {"text": "Snornabase ID", "number": 34},
    "bioparadigms_slc": {"text": "Bioparadigms", "number": 35},
    "orphanet": {"text": "Orphanet ID", "number": 36},
    "pseudogene.org": {"text": "pseudogene ID", "number": 37},
    "horde_id": {"text": "Horde id", "number": 38},
    "merops": {"text": "Merops", "number": 39},
    "imgt": {"text": "IMGT", "number": 40},
    "iuphar": {"text": "IUPHAR", "number": 41},
    "kznf_gene_catalogmamit-trnadb": {"text": "KZNF", "number": 42},
    "cd": {"text": "CD Name", "number": 43},
    "lncrnadb": {"text": "LncRNA Db", "number": 44},
    "enzyme_id": {"text": "Enzyme ID", "number": 45},
    "intermediate_filament_db": {"text": "Intermediate Filament Db", "number": 46},
    "rna_central_ids": {"text": "RNA Central ID", "number": 47},
    "lncipedia": {"text": "LncIpedia", "number": 48},
    "gtrnadb": {"text": "gtRNA db", "number": 49},
    "agr": {"text": "AGR", "number": 50},
    "mane_select": {"text": "MANE Select ID", "number": 51},
    "gencc": {"text": "GENCC", "number": 52}
}

def fetch_ids(infile, id_column_index, fetch_texts, db_config, outfile):
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        cursor = connection.cursor()

        # Read input file and extract entries
        if infile.endswith('.gz'):
            with gzip.open(infile, 'rt') as f:
                header = f.readline().strip().split("\t")
                entries = [line.strip().split("\t") for line in f]
        else:
            with open(infile, 'r') as f:
                header = f.readline().strip().split("\t")
                entries = [line.strip().split("\t") for line in f]

        # Check if id_column_index is valid
        if id_column_index < 0 or id_column_index >= len(header):
            print(f"Invalid column index {id_column_index}. Please provide a valid column index.")
            return

        # Get the unique entries from the specified column
        unique_entries = list(set(entry[id_column_index] for entry in entries))

        # Fetch column names from the database
        cursor.execute("SHOW COLUMNS FROM data_table")
        db_columns = [row[0] for row in cursor.fetchall()]

        # Determine the best match column in the database
        best_match_column = None
        max_matches = 0
        for column in db_columns:
            cursor.execute(f"SELECT COUNT(*) FROM data_table WHERE `{column}` IN ({','.join(['%s'] * len(unique_entries))})", unique_entries)
            matches = cursor.fetchone()[0]
            if matches > max_matches:
                max_matches = matches
                best_match_column = column

        if not best_match_column:
            print("No matching column found in the database.")
            return

        # Construct the SQL query
        fetch_columns = ', '.join([f"`{fetch_text}`" for fetch_text in fetch_texts])
        sql_query = f"SELECT {fetch_columns} FROM data_table WHERE `{best_match_column}` = %s"

        # Fetch entries and write to outfile
        if outfile.endswith('.gz'):
            with gzip.open(outfile, 'wt') as f:
                f.write(f"{'\t'.join(header)}\t{'\t'.join(fetch_texts)}\n")
                for entry in tqdm(entries, desc="Processing entries"):
                    cursor.execute(sql_query, entry[id_column_index])
                    fetched_data = cursor.fetchone()
                    if fetched_data:
                        fetched_data = "\t".join(map(str, fetched_data))  # Convert fetched data to a tab-separated string
                    else:
                        fetched_data = "\t".join(["Not Found"] * len(fetch_texts))
                    f.write(f"{'\t'.join(entry)}\t{fetched_data}\n")
        else:
            with open(outfile, 'w') as f:
                f.write(f"{'\t'.join(header)}\t{'\t'.join(fetch_texts)}\n")
                for entry in tqdm(entries, desc="Processing entries"):
                    cursor.execute(sql_query, entry[id_column_index])
                    fetched_data = cursor.fetchone()
                    if fetched_data:
                        fetched_data = "\t".join(map(str, fetched_data))  # Convert fetched data to a tab-separated string
                    else:
                        fetched_data = "\t".join(["Not Found"] * len(fetch_texts))
                    f.write(f"{'\t'.join(entry)}\t{fetched_data}\n")

    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch desired IDs and append to the input file.")
    parser.add_argument("--infile", help="Path to the input file", required=True)
    parser.add_argument("--id-column-index", type=int, help="Column index in the input file to use for fetching IDs", required=True)
    parser.add_argument("--fetch", help="Number corresponding to IDs as per the Fetch Table", required=True, nargs='+')
    parser.add_argument("--outfile", help="Path to the output file, if gzip desired output desired simply ad *.gz extension", required=True)

    args = parser.parse_args()

    # Convert fetch arguments to lowercase for case-insensitive comparison
    fetch_args_lower = [fetch_arg.lower() for fetch_arg in args.fetch]

    # Validate fetch arguments
    fetch_texts = []
    for fetch_arg_lower in fetch_args_lower:
        found_fetch = None
        for key, option in fetch_options.items():
            if key.lower() == fetch_arg_lower or str(option["number"]) == fetch_arg_lower:
                found_fetch = key
                fetch_texts.append(fetch_options[found_fetch]["text"])
                break

        if found_fetch is None:
            print(f"Invalid fetch argument: {fetch_arg_lower}. Please use one of the following:")
            for key in fetch_options.keys():
                print(key)
            exit(1)

    # Fetch IDs and write to the output file
    fetch_ids(args.infile, args.id_column_index, fetch_texts, db_config, args.outfile)

