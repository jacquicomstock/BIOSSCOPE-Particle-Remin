#load package
library(dada2)

#set working directory (tell R where to look for files)
setwd("/home/carlsonlab/SBCSS/fastqs/PR")
#create vector that denotes path
path <- "/home/carlsonlab/SBCSS/fastqs/PR"

#sort our fastq files into forward (R1) and reverse (R2) reads 
fnFs <- sort(list.files(path, pattern="_R1_001.fastq", full.names = TRUE))
fnRs <- sort(list.files(path, pattern="_R2_001.fastq", full.names = TRUE))

#pull out our sample names
sample.names <- sapply(strsplit(basename(fnFs), "_L"), `[`, 1)

#filter our samples
filt_path <- file.path(path, "filtered")
filtFs <- file.path(filt_path, paste0(sample.names, "_F_filt.fastq"))
filtRs <- file.path(filt_path, paste0(sample.names, "_R_filt.fastq"))

#trim the end of the sequences off that are low quality
for(i in seq_along(fnFs)) {
  fastqPairedFilter(c(fnFs[i], fnRs[i]), c(filtFs[i], filtRs[i]),
                    truncLen=c(240,175), 
                    maxN=0, maxEE=c(2,2), truncQ=2, rm.phix=TRUE,
                    compress=TRUE, verbose=TRUE)
}

#dereplicate our sequences (pull out 1 copy of each sequence)
derepFs <- derepFastq(filtFs, verbose=TRUE)
derepRs <- derepFastq(filtRs, verbose=TRUE)

#use sample names with newly created dereplicated samples
names(derepFs) <- sample.names
names(derepRs) <- sample.names

#GET RID OF SEQUENCER ERROR TO PRODUCE EXACT DNA SEQUENCES (ASVs)
#calculates/learns error rates in these samples
dadaFs.lrn <- dada(derepFs, err=NULL, selfConsist = TRUE, multithread=TRUE)
errF <- dadaFs.lrn[[1]]$err_out
dadaRs.lrn <- dada(derepRs, err=NULL, selfConsist = TRUE, multithread=TRUE)
errR <- dadaRs.lrn[[1]]$err_out
#save error files
saveRDS(errF, "errF.rds")
saveRDS(errR, "errR.rds")
#Denoise our samples with calculated error from previous step
dadaFs <- dada(derepFs, err=errF, multithread=TRUE)
dadaRs <- dada(derepRs, err=errR, multithread=TRUE)
#save files
saveRDS(dadaFs, "dadaFs_N.rds")
saveRDS(dadaRs, "dadaRs_N.rds")

#merge our forward and reverse reads into one long read
mergers <- mergePairs(dadaFs, derepFs, dadaRs, derepRs, verbose=TRUE)
saveRDS(mergers, "dadaFs_N.rds")

#create table of DNA sequences in each sample
seqtab <- makeSequenceTable(mergers[names(mergers) != "Mock"])
#look at dimensions of this dataframe
dim(seqtab)
table(nchar(getSequences(seqtab)))

#Remove DNA chimeras from dataset
seqtab.nochim <- removeBimeraDenovo(seqtab, verbose=TRUE)
sum(seqtab.nochim)/sum(seqtab)
dim(seqtab.nochim)

#save our sequences in dataframe
saveRDS(seqtab.nochim, "dadaFs_Nseqtab.nochim.rds")

#assign taxonomy to DNA sequences usings SILVA reference database
taxa <- assignTaxonomy(seqtab.nochim, "/home/carlsonlab/SBCSS/fastqs/silva_nr99_v138.1_wSpecies_train_set.fa.gz")
#look at most abundant taxonomy
unname(head(taxa))

#save taxa
saveRDS(taxa, "taxa.rds")

#write our abundance table
write.table(cbind(t(seqtab.nochim) , taxa), "PR_seqtab-nochimtaxa.txt", sep="\t", row.names=TRUE, col.names=NA, quote=FALSE)
#write our taxa file
write.table(taxa,"PR_taxa.txt", sep="\t", row.names=TRUE, col.names=NA, quote=FALSE)
