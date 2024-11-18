#fastq files downloaded from illumina have fastqs for each sample in individual files. First stepis to move all the fastqs to one folder
destination="/home/mobaxterm/Desktop/Research/Projects/BIOSSCOPE/AE2408/AE2408_Fastqs/redemultiplexed"
source="/home/mobaxterm/Desktop/Research/Projects/BIOSSCOPE\AE2408/AE2408_Fastqs/redemultiplexed/AE2408_02-434419108/FASTQ_Generation_2024-10-10_14_55_02Z-778616183/"

# Loop through each folder in the source directory
for folder in "$source"*/; do
    # Move all files from the current folder to the destination
    mv "$folder"* "$destination"
done

#upload files to local cluster
scp /home/mobaxterm/Desktop/Research/Projects/BIOSSCOPE/AE2408/AE2408_Fastqs/JCCC091924* carlsonlab@pod.cnsi.ucsb.edu:/home/carlsonlab/PR2
scp /home/mobaxterm/Desktop/Research/Projects/BIOSSCOPE/Pump_Size_Fraction_BIOSSCOPE/BIOSSCOPE_Pump_ASV_data/BIOS_Frac_Fastq/BIOSSCOPE _Size_Frac_fastq carlsonlab@pod.cnsi.ucsb.edu:/home/carlsonlab/BIOS_Frac/all_fastq

#SSH for the carlsonlab shared cluster and type in the password
ssh carlsonlab@pod.cnsi.ucsb.edu

#cd into the correct directory
cd PR

#create .R file
nano dada2_PR.R

#if a file already exists, copy & paste a copy of the file into the new directory
cp dada2_PR2.R /home/carlsonlab/BIOS_Frac/all_fastq

#move files into separate folders for separate jobs
mv /home/carlsonlab/PR2/JCCC091924-PC* /home/carlsonlab/PR2/AE2408_pump/
mv /home/carlsonlab/PR2/AE2408_pump/JCCC091924-PC* /home/carlsonlab/BIOS_Frac/all_fastq/

#activate conda environment with R
conda activate R4.2.0

#queue a job in slurm using sbatch
sbatch \
	--job-name=PR2v4 \
	--nodes=1 \
	--tasks-per-node=32 \
	--cpus-per-task=1 \
	--mem=32G \
	--time=5:00:00 \
	-o dada2_outv4 \
	-e dada2_errv4 \
	--wrap="Rscript dada2_PR2.R /home/carlsonlab/PR2"

 sbatch \
	--job-name=AE2408_pumpv6 \
	--nodes=1 \
	--tasks-per-node=32 \
	--cpus-per-task=1 \
	--mem=32G \
	--time=5:00:00 \
	-o dada2_outv6 \
	-e dada2_errv6 \
	--wrap="Rscript dada2_AE2408pump.R /home/carlsonlab/PR2/AE2408"

  sbatch \
	--job-name=NBv3 \
	--nodes=1 \
	--tasks-per-node=32 \
	--cpus-per-task=1 \
	--mem=32G \
	--time=3:00:00 \
	-o dada2_outv3 \
	-e dada2_errv3 \
	--wrap="Rscript dada2_NB.R /home/carlsonlab/PR2/NB_fastq"

   sbatch \
	--job-name=MNv4 \
	--nodes=1 \
	--tasks-per-node=32 \
	--cpus-per-task=1 \
	--mem=32G \
	--time=1:00:00 \
	-o dada2_outv4 \
	-e dada2_errv4 \
	--wrap="Rscript dada2_MN.R /home/carlsonlab/PR2/mock_neg"

    sbatch \
	--job-name=PUMPv3 \
	--nodes=1 \
	--tasks-per-node=32 \
	--cpus-per-task=1 \
	--mem=64G \
	--time=24:00:00 \
	-o dada2_outv3 \
	-e dada2_errv3 \
	--wrap="Rscript dada2_PUMP.R /home/carlsonlab/BIOS_Frac/all_fastq"


#once dada2 has finished, download files from cluster to local computer (type this into a local terminal)
scp carlsonlab@pod.cnsi.ucsb.edu:/home/carlsonlab/PR2/PR2_seqtab-nochimtaxa.txt /home/mobaxterm/Desktop
scp carlsonlab@pod.cnsi.ucsb.edu:/home/carlsonlab/PR2/PR2_taxa.txt /home/mobaxterm/Desktop

scp carlsonlab@pod.cnsi.ucsb.edu:/home/carlsonlab/PR2/AE2408_pump/AE2408pump_seqtab-nochimtaxa.txt /home/mobaxterm/Desktop
scp carlsonlab@pod.cnsi.ucsb.edu:/home/carlsonlab/PR2/AE2408_pump/AE2408pump_taxa.txt /home/mobaxterm/Desktop

scp carlsonlab@pod.cnsi.ucsb.edu:/home/carlsonlab/PR2/NB_fastq/NB_seqtab-nochimtaxa.txt /home/mobaxterm/Desktop
scp carlsonlab@pod.cnsi.ucsb.edu:/home/carlsonlab/PR2/NB_fastq/NB_taxa.txt /home/mobaxterm/Desktop

scp carlsonlab@pod.cnsi.ucsb.edu:/home/carlsonlab/PR2/mock_neg/PRmockneg_seqtab-nochimtaxa.txt /home/mobaxterm/Desktop
scp carlsonlab@pod.cnsi.ucsb.edu:/home/carlsonlab/PR2/mock_neg/PRmockneg_taxa.txt /home/mobaxterm/Desktop
