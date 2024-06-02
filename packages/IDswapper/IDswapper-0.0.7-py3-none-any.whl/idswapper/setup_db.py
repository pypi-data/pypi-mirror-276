import pymysql
import gzip
import getpass

# Prompt for database connection details
DB_HOST = input("Enter MySQL host (default: 'localhost'): ") or 'localhost'
DB_USER = input("Enter MySQL user: ")
DB_PASS = getpass.getpass("Enter MySQL password: ")
DB_NAME = input("Enter database name: ")
DATA_FILE = input("Enter path to the gzipped data file: ")

# Column mapping from data_file.gz to SQL database
column_mapping = {
    "gene_stable_id": "gene_stable_id",
    "transcript_stable_id": "Ensembl Transcript ID",
    "protein_stable_id": "Ensembl Protein ID",
    "xref": "xref",
    "db_name": "db_name",
    "info_type": "info_type",
    "source_identity": "source_identity",
    "xref_identity": "xref_identity",
    "linkage_type": "linkage_type",
    "hgnc_id": "HGNC ID",
    "symbol": "Gene Symbol",
    "name": "Gene Description",
    "locus_group": "Locus Group",
    "locus_type": "Locus Type",
    "status": "Status",
    "location": "Chromosome Location",
    "location_sortable": "Chr loci sortable",
    "alias_symbol": "Gene Aliases",
    "prev_symbol": "Previous Symbol",
    "gene_group": "Gene Group",
    "gene_group_id": "Gene Group ID",
    "date_approved_reserved": "date_approved_reserved",
    "date_symbol_changed": "date_symbol_changed",
    "date_name_changed": "date_name_changed",
    "date_modified": "date_modified",
    "entrez_id": "Entrez Gene ID",
    "ensembl_gene_id": "Ensembl Gene ID",
    "vega_id": "VEGA ID",
    "ucsc_id": "UCSC ID",
    "ena": "ENA",
    "refseq_accession": "Refseq Accession",
    "uniprot_ids": "Uniprot ID",
    "pubmed_id": "Pubmed ID",
    "rgd_id": "RGD ID",
    "cosmic": "COSMIC Entry",
    "omim_id": "OMIM ID",
    "mirbase": "mirBase ID",
    "homeodb": "HomeoDB ID",
    "snornabase": "Snornabase ID",
    "bioparadigms_slc": "Bioparadigms",
    "orphanet": "Orphanet ID",
    "pseudogene.org": "pseudogene ID",
    "horde_id": "Horde id",
    "merops": "Merops",
    "imgt": "IMGT",
    "iuphar": "IUPHAR",
    "kznf_gene_catalogmamit-trnadb": "KZNF",
    "cd": "CD Name",
    "lncrnadb": "LncRNA Db",
    "enzyme_id": "Enzyme ID",
    "intermediate_filament_db": "Intermediate Filament Db",
    "rna_central_ids": "RNA Central ID",
    "lncipedia": "LncIpedia",
    "gtrnadb": "gtRNA db",
    "agr": "AGR",
    "mane_select": "MANE Select ID",
    "gencc": "GENCC"
}

# Connect to the MySQL server
connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS)
cursor = connection.cursor()

# Create database
print(f"Creating database '{DB_NAME}'...")
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
cursor.execute(f"USE {DB_NAME}")

# Create table with the required columns
create_table_query = """
CREATE TABLE IF NOT EXISTS data_table (
    `gene_stable_id` LONGTEXT,
    `Ensembl Transcript ID` LONGTEXT,
    `Ensembl Protein ID` LONGTEXT,
    `xref` LONGTEXT,
    `db_name` LONGTEXT,
    `info_type` LONGTEXT,
    `source_identity` LONGTEXT,
    `xref_identity` LONGTEXT,
    `linkage_type` LONGTEXT,
    `HGNC ID` LONGTEXT,
    `Gene Symbol` LONGTEXT,
    `Gene Description` LONGTEXT,
    `Locus Group` LONGTEXT,
    `Locus Type` LONGTEXT,
    `Status` LONGTEXT,
    `Chromosome Location` LONGTEXT,
    `Chr loci sortable` LONGTEXT,
    `Gene Aliases` LONGTEXT,
    `Previous Symbol` LONGTEXT,
    `Gene Group` LONGTEXT,
    `Gene Group ID` LONGTEXT,
    `date_approved_reserved` LONGTEXT,
    `date_symbol_changed` LONGTEXT,
    `date_name_changed` LONGTEXT,
    `date_modified` LONGTEXT,
    `Entrez Gene ID` LONGTEXT,
    `Ensembl Gene ID` LONGTEXT,
    `VEGA ID` LONGTEXT,
    `UCSC ID` LONGTEXT,
    `ENA` LONGTEXT,
    `Refseq Accession` LONGTEXT,
    `Uniprot ID` LONGTEXT,
    `Pubmed ID` LONGTEXT,
    `RGD ID` LONGTEXT,
    `COSMIC Entry` LONGTEXT,
    `OMIM ID` LONGTEXT,
    `mirBase ID` LONGTEXT,
    `HomeoDB ID` LONGTEXT,
    `Snornabase ID` LONGTEXT,
    `Bioparadigms` LONGTEXT,
    `Orphanet ID` LONGTEXT,
    `pseudogene ID` LONGTEXT,
    `Horde id` LONGTEXT,
    `Merops` LONGTEXT,
    `IMGT` LONGTEXT,
    `IUPHAR` LONGTEXT,
    `KZNF` LONGTEXT,
    `CD Name` LONGTEXT,
    `LncRNA Db` LONGTEXT,
    `Enzyme ID` LONGTEXT,
    `Intermediate Filament Db` LONGTEXT,
    `RNA Central ID` LONGTEXT,
    `LncIpedia` LONGTEXT,
    `gtRNA db` LONGTEXT,
    `AGR` LONGTEXT,
    `MANE Select ID` LONGTEXT,
    `GENCC` LONGTEXT
)
"""
cursor.execute(create_table_query)

# Drop existing indexes
for column_name, column_desc in column_mapping.items():
    index_name = f"idx_{column_name}"
    cursor.execute(f"SHOW INDEX FROM data_table WHERE Key_name = '{index_name}'")
    if cursor.fetchone():
        drop_index_query = f"DROP INDEX {index_name} ON data_table"
        cursor.execute(drop_index_query)

# Create indexes for frequently queried columns
print("Creating indexes, this may take a while, please wait until completion...")
for column_name, column_desc in column_mapping.items():
    if column_desc in [
        "Ensembl Transcript ID",
        "Ensembl Protein ID",
        "HGNC ID",
        "Gene Symbol",
        "Gene Description",
        "Chromosome Location",
        "Gene Aliases",
        "Entrez Gene ID",
        "Ensembl Gene ID",
        "VEGA ID",
        "UCSC ID",
        "Refseq Accession",
        "Uniprot ID",
        "Pubmed ID",
        "COSMIC Entry",
        "OMIM ID",
        "Orphanet ID",
        "CD Name",
        "RNA Central ID",
        "MANE Select ID"
    ]:
        index_name = f"idx_{column_name}"
        if column_desc in [
            "Ensembl Transcript ID",
            "Ensembl Protein ID",
            "HGNC ID",
            "Gene Symbol",
            "Gene Description",
            "Chromosome Location",
            "Gene Aliases",
            "Entrez Gene ID",
            "Ensembl Gene ID",
            "VEGA ID",
            "UCSC ID",
            "Refseq Accession",
            "Uniprot ID",
            "Pubmed ID",
            "COSMIC Entry",
            "OMIM ID",
            "Orphanet ID",
            "CD Name",
            "RNA Central ID",
            "MANE Select ID"
        ]:
            # Specify a reduced key length for TEXT columns to avoid exceeding the maximum limit
            create_index_query = f"CREATE INDEX {index_name} ON data_table (`{column_desc}`(255))"
        else:
            create_index_query = f"CREATE INDEX {index_name} ON data_table (`{column_desc}`)"
        cursor.execute(create_index_query)
        print(f"Index created on column '{column_desc}'")

# Load data from gzipped file and insert into the table
with gzip.open(DATA_FILE, 'rt', encoding='utf-8') as f:
    headers = f.readline().strip().split('\t')
    for line in f:
        parts = line.strip().split('\t')
        data = {}
        for i in range(len(parts)):
            if headers[i] in column_mapping:
                # Truncate data to 2024 characters if necessary
                truncated_data = parts[i][:2024] if len(parts[i]) > 2024 else parts[i]
                data[column_mapping[headers[i]]] = truncated_data
        
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join([f"`{key}`" for key in data.keys()])
        sql = f"INSERT INTO data_table ({columns}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {', '.join([f'`{k}` = VALUES(`{k}`)' for k in data.keys()])}"
        
        try:
            cursor.execute(sql, list(data.values()))
        except pymysql.err.DataError as e:
            print(f"Data too long error: {e}")
            print(f"Problematic data: {data}")
            raise

# Commit and close connection
connection.commit()
cursor.close()
connection.close()

