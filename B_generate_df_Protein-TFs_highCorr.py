import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt


def heatmap_plot(data, g, celltype):
    fig, ax = plt.subplots(figsize = (18,16))
    plt.subplots_adjust(left=0.3, bottom=0.05, right=0.8, top=0.9)
    plt.tick_params(axis='both', which='major', labelbottom = False, bottom=False, top = False, labeltop=True)
    ax = sns.clustermap(data, annot=False, cmap="YlGnBu")
    ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize = 16,  rotation=90)
    ax.set_yticklabels(ax.get_ymajorticklabels(), fontsize = 12) 
    ax.set_title("{} {} ".format(celltype,g), fontsize=20,  pad=20)
    fig = ax.get_figure()
    plt.show()
    return(fig)

celltype = "CD14_Mono"
DPYdir = "DPY_RNA0.03_P0.15"
cut_from = 50
cut_to = 1000
rootdir = "cutsize_50"

# path = "../{}/output/{}/{}".format(celltype, DPYdir, RFdir)
path = "./data/data_created"

path_out = os.path.join(path,"protein-TFs_higCorr")
if not os.path.exists(path_out):
    os.makedirs(path_out)
  
path_in = path

df_P = pd.read_csv(os.path.join(path_in, "P_1-1.csv"), index_col=0)

proteins_all = list(df_P.columns)

df_corr = pd.read_csv(os.path.join(path, "correlation_all_{}~{}_withGroup.csv".format(cut_from, cut_to)), index_col=0)
df_corr.columns = df_corr.columns.str.replace("-", ".")


corrCut = 0.75
from tqdm import tqdm

for protein in tqdm(proteins_all):
    tfs = []
    pairs = []
    for pair in df_corr.columns[:-1]:
        if sum(abs(df_corr[pair])>corrCut) ==0 : continue
        
        (pro, tf) = pair.split("_")
        if pro != protein: continue
        
        pairs.append(pair)
        tfs.append(tf)
    
    
    if len(tfs) > 2 :
        # print(protein, "- TFs:", len(tfs))
        df_plt = df_corr[pairs]
        df_plt.index = df_corr['group']
        df_plt.columns = tfs
    
        df_plt.to_csv(os.path.join(path_out, "{}-TFs_highCorr.csv".format(protein)))
        
        
