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
scp carlsonlab@pod.cnsi.ucsb.edu:/home/carlsonlab/SBCSS/fastqs/SBCSS/PR_seqtab-nochimtaxa.txt /home/mobaxterm/Desktop/SBCSS
scp carlsonlab@pod.cnsi.ucsb.edu:/home/carlsonlab/SBCSS/fastqs/SBCSS/PR_taxa.txt /home/mobaxterm/Desktop/SBCSS
