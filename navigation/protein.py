import pandas as pd
import stringdb
import streamlit as st

def get_ppi_edge_list(gene, size):
    # """
    # Generate a list of all edges from the SIGNOR Protein-Protein interaction graph
    # SIGNOR tsv download: https://signor.uniroma2.it/downloads.php
    # SNAP download: https://snap.stanford.edu/biodata/datasets/10000/10000-PP-Pathways.html
    # """

    # signor_ppi = pd.read_csv('./assets/db/SIGNOR_PPI.tsv', sep='\t')
    # edges = signor_ppi.query('TYPEA == "protein" or TYPEB == "protein"')[['ENTITYA', 'ENTITYB', 'SCORE']].dropna()
    # edges = edges.loc[(~edges.ENTITYA.str.contains('"'))] #filter out non gene entries 
    # edges = edges[edges['ENTITYA'] != edges['ENTITYB']]
    
    # string_ids = stringdb.get_string_ids('B7-H4')
    # enrichment_df = stringdb.get_interaction_partners(string_ids.queryItem)
    
    genes = [gene]
    string_ids = stringdb.get_string_ids(genes)
    enrichment_df = stringdb.get_interaction_partners(string_ids.queryItem, limit=size)
    
    return string_ids.annotation.values[0], enrichment_df[['preferredName_A',	'preferredName_B']].values