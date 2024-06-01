# IDswapper
Convert given gene IDs to various other IDs. (under development, please come back later)

**Usage**
<br>``$ IDswapper --infile test.txt --id-column-index 0 --fetch "25" "5" "10" --outfile append_test.txt  ``</br>

For large files that are gzip compressed
<br>``$ IDswapper --infile test.tsv.gz --id-column-index 0 --fetch "25" "5" "10" --outfile append_test.tsv.gz``</br>

The ``--id-column-index`` allows query by picking any column in large files with many columns



**Fetch Table**
<br>These are the options supported for the ``--fetch `` argument</br> More options will be released in the next update

| Fetch Argument | Columns to be appended |
|---|---|
| 2 | Ensembl Transcript ID |
| 3 | Ensembl Protein ID |
| 4 | HGNC ID |
| 5 | Gene Symbol |
| 6 | Gene Description |
| 10 | Chromosome Location |
| 12 | Gene Aliases |
| 18 | Entrez Gene ID |
| 19 | Ensembl Gene ID |
| 20 | VEGA ID |
| 21 | UCSC ID |
| 23 | Refseq Accession |
| 25 | Uniprot ID |
| 30 | COSMIC Entry |
| 31 | OMIM ID |
| 36 | Orphanet ID |
| 43 | CD Name |
| 47 | RNA Central ID |
| 51 | MANE Select ID |

**Example**


<br>1. Input file </br>
| Entries | 
|---|
| ENSG00000075624 | 
| ENSG00000146648 | 
| ENSG00000141510 |

<br>2. Execute idswapper tool</br>
<br>``$ IDswapper --infile test.txt --id-column-index 0 --fetch "25" "5" "10" --outfile append_test.txt``</br>

<br>3. Output file </br>
| Fetch Argument | Uniprot ID | Gene Symbol | Chromosome Location |
|---|---|---|---|
| ENSG00000075624 | P60709 | ACTB | 7p22.1 |
| ENSG00000146648 | P00533 | EGFR | 7p11.2 |
| ENSG00000141510 | P04637 | TP53 | 17p13.1 |

<br></br>

**INSTALLATION**
<br>`` $ pip install IDswapper ``</br>
