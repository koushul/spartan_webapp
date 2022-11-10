from pathlib import Path

import pandas as pd
import streamlit as st

from pathlib import Path
import random

cutsize_from = 30
cutsize_to = 10000

fuzzy_match = lambda root, fname: list(root.glob(fname))[0]

@st.cache
def litcov_search(search):
    lines = []
    try:
        with open(f'./litcovid/tsv?text={search}', 'r') as f:
            lines = f.readlines()[33:]
        if lines:
            litcovdf = pd.DataFrame([x.split('\t') for x in lines[1:]], 
                    columns=['pmid', 'title', 'journal']).applymap(lambda x: x.replace('\n', ''))
            return litcovdf
        else:
            return pd.DataFrame([])
    
    except FileNotFoundError:
        return pd.DataFrame([])



class Dataset:
    
    metadata = {
        'name': ['E-MTAB-9357', 'GSE155673', 'meyer21_pbmc', 'GSE167118'],
        'organism': ['Homo sapiens', 'Homo sapiens', 'Homo sapiens', 'Homo sapiens'],
        'patients': [270, 12, 143, 93],
        'cell count': ['559,517', '59,664', '691,683', '86,935'],
        'assay': ['CITE-seq', 'CITE-seq', 'CITE-seq', 'CITE-seq'],
        'surface proteins': [random.randint(10, 100), 34, random.randint(10, 100), random.randint(10, 100)],
        'transcription factors': [random.randint(10, 100), 206, random.randint(10, 100), random.randint(10, 100)],
        'pmid': [33171100,  54371, 33879890, 33622974],
        'severity': ['Healthy, Mild, Moderate, Severe']*4,
        'url': [
            'https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-9357',
            'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE155673', 
            'https://www.covid19cellatlas.org/index.patient.html', 
            'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE167118'
        ],
        'title': [
            'Multiomic Immunophenotyping Of COVID-19 Patients Reveals Early Infection Trajectories',
            'Systems Biological Assessment Of Immunity To Mild Versus Severe COVID-19 Infection In Humans',
            'The Cellular Immune Response To COVID-19 Deciphered By Single Cell Multi-Omics Across 2 Three UK Centres',
            'Clonal expansion and activation of tissue-resident memory-like Th17 cells expressing GM-CSF in the lung of severe COVID-19 patients'
        ]
    }
    
    def __init__(self, root):
        self.root = root
        self.name = self.root.name
        self.cell_types = [i.name for i in self.root.iterdir()]
        # st.write(self.root, self.cell_types)
        
        self.umap = str(Path('./data/umaps/') / f'{self.name} dataset UMAP.png')
        self.meta = pd.DataFrame(self.metadata)
    
    @classmethod
    def metadata_df(cls):
        return pd.DataFrame(cls.metadata)
    
        
    def surface_proteins(self, cell_type):
        proteins = (self.root / cell_type / 'protein-TFs_higCorr' / 'Figure').iterdir()
        proteins = [i.name.split('~TFs_highCorr_corrcut_')[0] for i in proteins]
                
        return proteins
    
    @property
    def total_surface_proteins(self):
        proteins = set()
        for ct in self.cell_types:
            for p in pd.read_csv(fuzzy_match((self.root / ct), 'proteins_all_*~*_withGroup.csv')).columns:
                proteins.add(p)
        proteins = proteins.difference({'Unnamed: 0', 'group'})
        return proteins
    
    @property
    def total_transcription_factors(self):
        tfs = set()
        for ct in self.cell_types:
            
            for p in pd.read_csv(fuzzy_match((self.root / ct), 'proteins_all_*~*_withGroup.csv')).columns:
                tfs.add(p)
        tfs = tfs.difference({'Unnamed: 0', 'group'})
        return tfs
    
    def transcription_factors(self, cell_type):
        tfs = (self.root / cell_type / 'TF-proteins_higCorr' / 'Figure').iterdir()
        tfs = [i.name.split('~proteins_highCorr_corrcut_')[0] for i in tfs]
        return tfs
    
    def get_protein_tf_data(self, cell_type, protein):
        base = self.root / cell_type / 'protein-TFs_higCorr'
        img =  list((base / 'Figure').glob(f'{protein}~TFs_highCorr*'))[0]
        csv = list((base).glob(f'{protein}~TFs_highCorr*.csv'))[0]
        return (str(csv), str(img))
    
    def get_tf_protein_data(self, cell_type, tf):
        base = self.root / cell_type / 'TF-proteins_higCorr'
        img =  list((base / 'Figure').glob(f'{tf}~proteins_highCorr_corrcut_*'))[0]        
        csv = list((base).glob(f"{tf}~proteins_highCorr_corrcut_*.csv"))[0]
        return (str(csv), str(img))
    
    
    def get_tf_df(self, celltype, protein):
        df_data = pd.read_csv(fuzzy_match((self.root / celltype), 'TFs_rank_all_*~*_withGroup.csv'))
        df_plt = pd.DataFrame([df_data.group, df_data[protein]]).T
        df_plt.columns = ['patient_group', 'Pair_correlations']
        return df_plt
    
    def get_protein_df(self, celltype, protein):
        df_data = pd.read_csv(fuzzy_match((self.root / celltype), 'proteins_all_*~*_withGroup.csv'))
        df_plt = pd.DataFrame([df_data.group, df_data[protein]]).T
        df_plt.columns = ['patient_group', 'Pair_correlations']
        return df_plt
    
    

class Datacore:
    
    def __init__(self):
        self.root_path = Path('./data/')
        self.datasets = [Dataset(i) for i in (self.root_path / 'data').iterdir()]
        self.name2ds = dict(zip([ds.name for ds in self.datasets], self.datasets))
        
        
    # def get_protein_tf_data(self, ds, cell_type):
    #     return self.name2dsp[ds].get_protein_tf_data(cell_type, pair)
        


# @st.experimental_singleton
def make_datacore():
    return Datacore