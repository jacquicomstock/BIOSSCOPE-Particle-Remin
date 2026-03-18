library(dplyr)
library(readr)

setwd("C:/Users/jacqu/Desktop/Research/Projects/BIOSSCOPE/Particle_Experiments/Joined_Files/16S")

# load file
df <- read_csv("merged_PR_PR2_PR3_ASV_taxa_wbyfambygen.csv")

#sum by genus
genus_summed <- df %>%
  select(-c(Kingdom, Phylum, Class, Order, Family, Genus, Species, Taxa_by_family)) %>%
  group_by(Taxa_by_genus) %>%
  summarise(across(where(is.numeric), ~ sum(.x, na.rm = TRUE)), .groups = "drop")

#sum by family
family_summed <- df %>%
  select(-c(Kingdom, Phylum, Class, Order, Family, Genus, Species, Taxa_by_genus)) %>%
  group_by(Taxa_by_family) %>%
  summarise(across(where(is.numeric), ~ sum(.x, na.rm = TRUE)), .groups = "drop")

#save files
write_csv(genus_summed, "merged_PR_PR2_PR3_ASV_summed_by_genus.csv")
write_csv(family_summed, "merged_PR_PR2_PR3_ASV_summed_by_family.csv")
