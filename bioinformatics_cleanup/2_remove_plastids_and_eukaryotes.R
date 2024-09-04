#load packages
library(dplyr)

#remove eukaryotes, chloroplasts and mitochondria
count_tab <- read.csv("PR_seqtab-nochimtaxa.csv", header=TRUE,sep=",",row.names=1, na.strings = "NOPE")
tax_tab <- read.csv("PR_taxa.csv", header=TRUE,sep=",", row.names = 1, na.strings = "NOPE")

#Remove rows with chloroplast as the Order name
ASV_nochl <- count_tab %>% filter(Order !="Chloroplast")
TAX_nochl <- tax_tab %>% filter(Order !="Chloroplast")

#Remove rows with mitochondria as the Family name
ASV_nochl.mit <- ASV_nochl %>% filter(Family !="Mitochondria")
TAX_nochl.mit <- TAX_nochl %>% filter(Family !="Mitochondria")

#Remove rows with Eukaryotes as the Kingdom name
ASV_nochl.mit.euk <- ASV_nochl.mit %>% filter(Kingdom !="Eukaryota")
TAX_nochl.mit.euk <- as.matrix(TAX_nochl.mit %>% filter(Kingdom !="Eukaryota"))

#write new files
write.csv(ASV_nochl.mit.euk, file="PR_seqtab-nochimtaxa_NoChlMitEuk.csv", row.names=T)
write.csv(TAX_nochl.mit.euk, file="PR_taxa_NoChlMitEuk.csv", row.names=T)
