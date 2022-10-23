import stringdb
import random

def generate_color():
    random_number = random.randint(0,16777215)
    hex_number = str(hex(random_number))
    hex_number ='#'+ hex_number[2:]
    return hex_number
        
def get_ppi_edge_list(gene, neighbors, size):
    genes = [gene]
    string_ids = stringdb.get_string_ids(genes)
    enrichment_df = stringdb.get_interaction_partners(string_ids.queryItem, limit=size)
    extras = list(enrichment_df['preferredName_B'].values[:neighbors])
    string_ids = stringdb.get_string_ids(extras+genes)
    enrichment_df = stringdb.get_interaction_partners(string_ids.queryItem, limit=size)

    return string_ids, enrichment_df[['preferredName_A',	'preferredName_B', 'score']].values