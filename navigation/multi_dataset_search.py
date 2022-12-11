import streamlit as st

def multi_dataset_page(datacore):
    st.info("""
        Discover transcription factors that are consistently and significantly different between healthy vs impacted patients
            
    """)
    
    thresh = st.slider('p-value threshold', min_value=0.0, max_value=0.5, value=0.05, step=0.01)
    
    names = list(datacore.name2ds.keys())
    datasets = st.multiselect('Datasets', names, [names[0], names[1]])
    
    if len(datasets) < 1:
        st.error('Please select at least one dataset.')
        
    else:
        common_celltypes = set.intersection(*[set(datacore.name2ds[ds].celltypes) for ds in datasets])    
        results = {} 
        
        my_bar = st.progress(0)
        
        with st.spinner(f'👀 Looking for tfs across {len(datasets)} datasets... (p-value < {thresh})'):
            for idx, ct in enumerate(common_celltypes):
                results[ct] = {}
                for ds in datasets:
                    results[ct][ds] = {}
                    tfs = list(datacore.name2ds[ds].transcription_factors(ct))
                    for tf in tfs:
                        try:
                            pval, adj_pval = datacore.name2ds[ds].get_tf_pvals(ct, tf)
                        except IndexError:
                            pval = 1.0
                        if pval < thresh:
                            results[ct][ds][tf] = pval
                my_bar.progress((idx)/(len(common_celltypes)-1))
                        
        celebrate = False                  
        for ct in common_celltypes:
            significant_tfs = set.intersection(*[set(results[ct][ds].keys()) for ds in datasets])
            if len(significant_tfs)>0:
                celebrate = True
                st.markdown('## '+ct)
                st.write(significant_tfs)
                
                cols = st.columns(len(datasets))
                
                for stf in significant_tfs:
                    for col, ds in zip(cols, datasets):
                        col.metric(label=f'{stf} | {ds}', value = round(results[ct][ds][stf], 4), help='p-value computed using wilcox test')
                        
                st.markdown('---')
                
        # if celebrate:
        #     st.balloons()