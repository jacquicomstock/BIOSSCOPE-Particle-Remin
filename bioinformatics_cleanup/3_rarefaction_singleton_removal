#load packages
library(phyloseq)

#load data
ASV_nochl.mit.euk <- read.csv("PR_seqtab-nochimtaxa_NoChlMitEuk.csv", header=TRUE,sep=",",row.names=1, na.strings = "NOPE")
TAX_nochl.mit.euk <- read.csv("PR_taxa_NoChlMitEuk.csv", header=TRUE,sep=",", row.names = 1, na.strings = "NOPE")
meta <- read.csv("SBCSS_metadata.csv", header=TRUE,sep=",",row.names=1)

#generate rarefaction curve
ASV <- ASV_nochl.mit.euk[,1:(ncol(ASV_nochl.mit.euk)-7)]
rarecurve(tASV, step = 1000, col = "blue", label=F, xlim=c(0,20000))

#rarefy samples to 11000
OTU <- otu_table(ASV, taxa_are_rows = T)
TAX <- tax_table(TAX_nochl.mit.euk)
MET <- sample_data(meta)
phy <- phyloseq(OTU,TAX,MET)

set.seed(8800)
rar <- rarefy_even_depth(phy, sample.size = 11000)
ASV_rar <- rar@otu_table
TAX_rar <- rar@tax_table
MET_rar <- rar@sam_data

#calculate relative abundance
ASV_rar_prop <- apply(ASV_rar, 2, function(x) x/sum(x)*100)

#remove singletons (1/11000*100=0.0091%)
single <- rowSums(ASV_rar_prop[,1:ncol(ASV_rar_prop)]) > 0.0091
ASV_NoSingle <- as.data.frame(ASV_rar_prop[single,])

#Remove singletons from rarefied taxonomy file
ASVrow <- as.data.frame(rownames(ASV_NoSingle))
colnames(ASVrow) <- "ASV"
taxa_rar <- as.data.frame(TAX_rar)
taxa_rar$ASV <- rownames(taxa_rar)
taxa_NoSingle <- inner_join(taxa_rar,ASVrow, by="ASV")

#create trimmed/rarefied metadata table
sample_rar <- as.data.frame(colnames(ASV_NoSingle))
colnames(sample_rar) <- "Sample"
sample_rar$Sample <- gsub('_','.', sample_rar$Sample)

meta$Sample <- rownames(meta)
meta$Sample <- gsub('_','.', meta$Sample)
meta_all <- full_join(sample_rar,meta, by= "Sample")
meta_rar <- inner_join(sample_rar, meta, by="Sample")

#write new ASV and taxa file
write.csv(taxa_NoSingle, file="PR_taxa_rar13000_NoSingle.csv")
write.csv(ASV_NoSingle, file="PR_seqtab-nochimtaxa_rar13000_NoSingle.csv")
write.csv(meta_rar,file="PR__meta_rar13000.csv")
