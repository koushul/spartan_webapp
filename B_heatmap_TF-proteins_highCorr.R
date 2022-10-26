
library(pheatmap)

rm(list=ls())
# setwd(system("pwd", intern = T) )
dir = dirname(rstudioapi::getSourceEditorContext()$path)
setwd(dir)

cutsize_from = 50
cutsize_to = 10000
celltype = "CD14_Mono"
DPYdir = "DPY_RNA0.03_P0.15"
rootdir = "cutsize_50"
# path = sprintf("./%s/%s/%s/data_created/TF-Proteins_higCorr",celltype,DPYdir, rootdir)
path = "/Users/koushulramjattun/Downloads/spartan_webapp-1/data/data_created/protein-TFs_higCorr"
path_fig = file.path(path, "Figure")
dir.create(path_fig, showWarnings = TRUE,  recursive = TRUE)

save_pheatmap_pdf <- function(x, filename, width=1200, height=1500) {
  stopifnot(!missing(x))
  stopifnot(!missing(filename))
  png(filename, width = width, height=height, res=150)
  grid::grid.newpage()
  grid::grid.draw(x$gtable)
  dev.off()
}

filenames = list.files(path)

for (filename in filenames){
  if (filename=="Figure" | filename=="table_size.xlsx"){next}
  df= read.csv(file.path(path,filename))
  if (ncol(df) == 0 ) {next}
  df_plt = as.matrix(t(df[,2:ncol(df)]))
  colnames(df_plt) = seq(ncol(df_plt))
  
  annotation_col = data.frame(
    group = as.factor(df[,1]))
  
  # rownames(annotation_col) = paste0(as.character(df[,1]),seq(nrow(df)))
  
  xx = pheatmap(df_plt, annotation_col  = annotation_col, show_colnames=FALSE, main=substr(filename,1,nchar(filename)-4 ))
  save_pheatmap_pdf(xx, file.path(path_fig, sprintf("%s.png", filename)))
  
}


