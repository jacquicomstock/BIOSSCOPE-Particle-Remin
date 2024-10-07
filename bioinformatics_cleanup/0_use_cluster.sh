#fastq files downloaded from illumina have fastqs for each sample in individual files. First stepis to move all the fastqs to one folder
destination="/home/mobaxterm/Desktop/Research/Projects/BIOSSCOPE/AE2408/AE2408_Fastqs/"
source="/home/mobaxterm/Desktop/Research/Projects/BIOSSCOPE/AE2408/AE2408_Fastqs/AE2408_01-434104849/FASTQ_Generation_2024-10-07_18_28_02Z-778256556/"

# Loop through each folder in the source directory
for folder in "$source"*/; do
    # Move all files from the current folder to the destination
    mv "$folder"* "$destination"

#upload files to local cluster
scp /home/mobaxterm/Desktop/Research/Projects/BIOSSCOPE/AE2408/AE2408_Fastqs/JCCC091924* user@remote.cluster.address:/home/user/target_directory/ carlsonlab@pod.cnsi.ucsb.edu:/home/carlsonlab/PR2

#SSH for the carlsonlab shared cluster and type in the password
ssh carlsonlab@pod.cnsi.ucsb.edu

#cd into the correct directory
cd PR

#create .R file
nano dada2_PR.R

#activate conda environment with R
conda activate R4.2.0

#queue a job in slurm using sbatch
sbatch \
	--job-name=PR \
	--nodes=1 \
	--tasks-per-node=32 \
	--cpus-per-task=1 \
	--mem=32G \
	--time=5:00:00 \
	-o dada2_out \
	-e dada2_err \
	--wrap="Rscript dada2_PR.R /home/carlsonlab/SBCSS/fastqs/PR"


#once dada2 has finished, download files from cluster to local computer (type this into a local terminal)
scp carlsonlab@pod.cnsi.ucsb.edu:/home/carlsonlab/SBCSS/fastqs/PR/PR_seqtab-nochimtaxa.txt /home/mobaxterm/Desktop
scp carlsonlab@pod.cnsi.ucsb.edu:/home/carlsonlab/SBCSS/fastqs/PR/PR_taxa.txt /home/mobaxterm/Desktop
