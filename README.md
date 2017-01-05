# Squatch in metagenomics
###2015-2017 BYU College of Life Sciences, Department of Biology, 
####Metagenomic research

# Procedure
### Prerequisite: 
		* have an mgrast account
		* install blast+ from ncbi
		* download the nt database
		* create a gorilla database from the gorilla3 genome

##MGRAST
1. Navigate to http://metagenomics.anl.gov/?page=Home
2. Log in
3. Click on the barchart icon in upper right corner of screen to go to the anaylsis page
4. For every metagenome of interest:
	* Select a metagenome
	* For every RNA Annotation Source (do not use M5RNA):
		* Select a RNA annotation Source
		* Change ```Max. e-Value Cutoff``` to -20
		* Change ```Min. % Identity Cutoff``` to 50
		* Change ```Min. Alignment Length Cutoff``` to 10
		* Select the radio button next ```barchart```
		* Generate
		* Navigate the barchart to *Eukaryota* -> *Chordata* -> *Mammalia* -> *Primates* -> *Hominidae*
		* Select ```to workbench``` next to *Genus Distribution (Hominidae)* to send features to workbench
		* Navigate to the Workbench tab
		* For every DNA/RNA annotation:
			* Download the annotated metagenome fasta file
#####At this point you should have a new directory full of fasta files from your metagenome that were identified as hominid
##Terminal
#####All of the following commands should be run from the directory that contains both the Scripts directory and the Fasta Directory
1. Run ```sortFastas.py <fasta_dir> <len cut-off>```
	- the fasta_dir is the directory containing your fasta files from the mgrast step
	- the <len cut-off> I ran and used was 100, which means if a sequence is less than 100 nucleotides long, its considered small
	- this script will produce a summary file which contains some data on the average sequence lengths so you can judge if your cutoff is appropriate
2. Run ```blastn.sh <directory_containing_sortedfna_files> <gorilla_db_name> <E-value>```
3. Run ```findFastas.py <directory_containing_blast_files> <directory_containing_sortedfna_files>```
	- this script with find the fasta files that matched something in blast
4. Run ```blastn.sh <directory_containing_found_fasta_files> nt <E-value>```
	- I used the same E-value as before
5. Navigate to the new nt_blast directory.

