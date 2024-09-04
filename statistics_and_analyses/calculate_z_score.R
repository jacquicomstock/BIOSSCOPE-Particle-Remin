#filter ASVs with less than 1% abundance in at least 2 samples
#set parameters tp cull bacterioplankton taxa to the more cosmopolitan taxa
ASV <- PR[,10:ncol(PR)]
meta <- PR[,1:9]
relabund.df <- as.data.frame(t((ASV/100)))

ASV_cull <- relabund.df %>%
  filter(rowSums(. > .01) >= 2)

#Calculate z score for abundant taxa
#make function for calculating standard deviation
zscore <- function(x) {
  (x-mean(x, na.rm = TRUE))/sd(x, na.rm = TRUE)
}

#apply function to every column in the ASV dataframe (make sure there are no metadata columns)
result <- apply(ASV_cull, 2, zscore)

#convert result back into a dataframe
result_df <- as.data.frame(t(result))

# Calculate averages by group
tRA_meta <- as.data.frame(cbind(meta$Treatment_Fraction_Timepoint, result_df))
colnames(tRA_meta)[1] <- "Treatment_Fraction_Timepoint"
averages <- aggregate(. ~Treatment_Fraction_Timepoint, tRA_meta, mean)
