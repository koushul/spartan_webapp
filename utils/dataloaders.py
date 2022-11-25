from pathlib import Path

import pandas as pd
import streamlit as st

from pathlib import Path
import random

import requests
from bs4 import BeautifulSoup
import re

from texts.references import CELL_NAMES, CELL_NAMES_REVERSE


cutsize_from = 30
cutsize_to = 10000

fuzzy_match = lambda root, fname: list(root.glob(fname))[0]


class Dataset:
    
    metadata = {
        'name': ['E-MTAB-9357', 'GSE155673', 'meyer21_pbmc', 'GSE167118'],
        'organism': ['Homo sapiens', 'Homo sapiens', 'Homo sapiens', 'Homo sapiens'],
        'patients': [270, 12, 143, 68],
        'cell count': ['559,517', '59,664', '691,683', '396,244'],
        'assay': ['CITE-seq', 'CITE-seq', 'CITE-seq', 'CITE-seq'],
        'surface proteins': [190, 38, random.randint(10, 100), 192],
        'transcription factors': [209, 206, random.randint(10, 100), random.randint(10, 100)],
        'pmid': [33171100,  54371, 33879890, 33622974],
        'severity': ['Healthy, Mild, Moderate, Severe']*4,
        'url': [
            'https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-9357', ## SU: E-MTAB-9357
            'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE155673', ## AR: GSE155673
            'https://www.covid19cellatlas.org/index.patient.html', ## 
            'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE167118' ## LIU: GSE167118
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
        self.celltypes = [CELL_NAMES.get(i.name, i.name) for i in self.root.iterdir()]
        self.umap = str(Path('./data/umaps/') / f'UMAP_{self.name}.png')
        self.meta = pd.DataFrame(self.metadata)
    
    @classmethod
    def metadata_df(cls):
        return pd.DataFrame(cls.metadata)
    
    
    def get_tf_pvals(self, celltype, protein):
        celltype = CELL_NAMES_REVERSE[celltype]
        pth =  str(self.root / celltype / 'TFrank_wilcox_pvalues_healthy2infected.csv')
        pvals = pd.read_csv(pth)
        _, pval, adj_pval = pvals[pvals.features_all==protein].values[0]
        return pval, adj_pval
    
    def get_protein_pvals(self, celltype, protein):
        celltype = CELL_NAMES_REVERSE[celltype]
        pth =  str(self.root / celltype / 'protein_wilcox_pvalues_healthy2infected.csv')
        pvals = pd.read_csv(pth)
        _, pval, adj_pval = pvals[pvals.features_all==protein].values[0]
        return pval, adj_pval
    
        
    def surface_proteins(self, celltype):
        celltype = CELL_NAMES_REVERSE[celltype]
        proteins = (self.root / celltype / 'protein-TFs_higCorr' / 'Figure').iterdir()
        proteins = [i.name.split('~TFs_highCorr_corrcut_')[0] for i in proteins]
        return proteins
    
    @property
    def total_surface_proteins(self):
        proteins = set()
        for ct in self.celltypes:
            ct = CELL_NAMES_REVERSE[ct]
            for p in pd.read_csv(fuzzy_match((self.root / ct), 'proteins_all_*~*_withGroup.csv')).columns:
                proteins.add(p)
        proteins = proteins.difference({'Unnamed: 0', 'group'})
        return proteins
    
    @property
    def total_transcription_factors(self):
        tfs = set()
        for ct in self.celltypes:
            ct = CELL_NAMES_REVERSE[ct]
            
            for p in pd.read_csv(fuzzy_match((self.root / ct), 'TFs_rank_all_*~*_withGroup.csv')).columns:
                tfs.add(p)
        tfs = tfs.difference({'Unnamed: 0', 'group'})
        return tfs
    
    def transcription_factors(self, celltype):
        celltype = CELL_NAMES_REVERSE[celltype]
        tfs = (self.root / celltype / 'TF-proteins_higCorr' / 'Figure').iterdir()
        tfs = [i.name.split('~proteins_highCorr_corrcut_')[0] for i in tfs]
        return tfs
    
    def get_protein_tf_data(self, celltype, protein):
        celltype = CELL_NAMES_REVERSE[celltype]
        base = self.root / celltype / 'protein-TFs_higCorr'
        img =  list((base / 'Figure').glob(f'{protein}~TFs_highCorr*'))[0]
        csv = list((base).glob(f'{protein}~TFs_highCorr*.csv'))[0]
        return (str(csv), str(img))
    
    def get_tf_target_gene_img(self, celltype, tf):
        celltype = CELL_NAMES_REVERSE[celltype]
        base = self.root / celltype / 'TF-mRNAs_highCorr' / 'Figure'
        img =  list(base.glob(f'{tf}~mRNAs_highCorr_corrcut_*'))[0]
        return str(img)
    
    
    def get_tf_protein_data(self, celltype, tf):
        celltype = CELL_NAMES_REVERSE[celltype]
        base = self.root / celltype / 'TF-proteins_higCorr'
        img =  list((base / 'Figure').glob(f'{tf}~proteins_highCorr_corrcut_*'))[0]        
        csv = list((base).glob(f"{tf}~proteins_highCorr_corrcut_*.csv"))[0]
        return (str(csv), str(img))
    
    
    def get_tf_df(self, celltype, protein):
        celltype = CELL_NAMES_REVERSE[celltype]
        df_data = pd.read_csv(fuzzy_match((self.root / celltype), 'TFs_rank_all_*~*_withGroup.csv'))
        df_plt = pd.DataFrame([df_data.group, df_data[protein]]).T
        df_plt.columns = ['patient_group', 'Pair_correlations']
        return df_plt
    
    
    def get_protein_df(self, celltype, protein):
        celltype = CELL_NAMES_REVERSE[celltype]
        df_data = pd.read_csv(fuzzy_match((self.root / celltype), 'proteins_all_*~*_withGroup.csv'))
        df_plt = pd.DataFrame([df_data.group, df_data[protein]]).T
        df_plt.columns = ['patient_group', 'Pair_correlations']
        return df_plt
    
    

class Datacore:
    
    def __init__(self):
        self.root_path = Path('./data/')
        self.datasets = [Dataset(i) for i in (self.root_path / 'data').iterdir()]
        self.name2ds = dict(zip([ds.name for ds in self.datasets], self.datasets))
        


# @st.experimental_singleton
def make_datacore():
    return Datacore