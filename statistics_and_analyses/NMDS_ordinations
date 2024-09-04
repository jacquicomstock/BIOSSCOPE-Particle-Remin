library(vegan)
library (ggplot)

#load dataframes
fulldf <- read.csv("PR_EnvASV_rar11000.csv", header=TRUE,sep=",",row.names=1)
RA <-fulldf[,10:ncol(fulldf)]
meta <- fulldf[,1:9]

#generate NMDS ordination of ALL samples
all.asin <- as.matrix(asin(sqrt(RA/100)))
all.nmds <- metaMDS(all.asin, distance = "bray", trymax=50)
ALL.scores = as.data.frame(scores(all.nmds))
write.csv(ALL.scores,"PR_ALL_NMDSscores.csv")

ggplot(data = ALL.scores, 
       mapping = aes(x=NMDS1, y=NMDS2))+ 
        geom_point(size=5, alpha=0.8, aes(shape=meta$Fraction_and_Timepoint, color = meta$Water_and_Treatment, stroke= 2))

#generate NMDS ordination of EXPERIMENTAL samples
PR <- filter(fulldf, Sample_type == "Experiment")
PR.RA <- PR[,10:ncol(PR)]
PR.meta <- PR[,1:9]
PR.asin <- as.matrix(asin(sqrt(PR.RA/100)))
PR.nmds <- metaMDS(PR.asin, distance = "bray", trymax=50)
PR.scores = as.data.frame(scores(PR.nmds))
write.csv(PR.scores,"PR_NMDSscores.csv")

ggplot(data = PR.scores, 
       mapping = aes(x=NMDS1, y=NMDS2))+ 
        geom_point(size=5, alpha=0.8, aes(shape = PR.meta$Fraction_and_Timepoint , color = PR.meta$Water_and_Treatment , stroke= 2))

#generate NMDS ordination of EXPERIMENTAL PARTICLE samples
PA <- filter(PR, Fraction == "3um")
PA.RA <- PA[,10:ncol(PA)]
PA.meta <- PA[,1:9]
PA.asin <- as.matrix(asin(sqrt(PA.RA/100)))
PA.nmds <- metaMDS(PA.asin, distance = "bray", trymax=50)
PA.scores = as.data.frame(scores(PA.nmds))
write.csv(PA.scores,"PR.PA_NMDSscores.csv")

ggplot(data = PA.scores, 
       mapping = aes(x=NMDS1, y=NMDS2))+ 
        geom_point(size=5, alpha=0.8, aes(shape = PA.meta$Fraction_and_Timepoint , color = PA.meta$Water_and_Treatment , stroke= 2))

#generate NMDS ordination of EXPERIMENTAL FREE LIVING samples
FL <- filter(PR, Fraction == "0.2um")
FL.RA <- FL[,10:ncol(FL)]
FL.meta <- FL[,1:9]
FL.asin <- as.matrix(asin(sqrt(FL.RA/100)))
FL.nmds <- metaMDS(FL.asin, distance = "bray", trymax=50)
FL.scores = as.data.frame(scores(FL.nmds))
write.csv(FL.scores,"PR.FL_NMDSscores.csv")

ggplot(data = FL.scores, 
       mapping = aes(x=NMDS1, y=NMDS2))+ 
        geom_point(size=5, alpha=0.8, aes(shape = FL.meta$Fraction_and_Timepoint , color = FL.meta$Water_and_Treatment , stroke= 2))
