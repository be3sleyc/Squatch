#! /usr/bin/env python
## author: Christian Beesley

import sys
import os
import numpy as np

usage = "usage: sortFasta.py {fasta_dir} {cutoff_len}\n"+\
"\t a script that takes a directory containing fasta files and a number\n"+\
"\t representing the length of a nucleotide sequence\n"+\
"\t requires:\n"+\
"\t\t -fasta_dir: a dir a directory containing the fasta files you want sorted\n"+\
"\t\t -cutoff_len: a number which is the minimum length you want included in the final sort\n"+\
"\t This script particularly looks for fasta files of Human, Gorilla, and Chimp."

def Average(some_list):
    if len(some_list) > 0:
        return sum(some_list) / len(some_list)
    else:
        return 0

def SpeciesSort(ids, species, species_file):
	species_count = []
	species_ids = filter(lambda x:species in x, ids.keys())
	for key in species_ids:
		species_file.write(key + "\n" + "\n".join(ids[key].strip("_").split("_")) + "\n")
		species_count.append(len("\n".join(ids[key].strip("_").split("_"))))
		del ids[key]
	species_file.close()
	return Average(species_count)

def main():
	if len(sys.argv) != 3:
		print "improper arguement quantity"
		print " ".join(sys.argv)
		print usage
		return
	else:
		fadir = sys.argv[1]
		if not os.path.isdir(fadir):
			print "please give a valid directory"
			print " ".join(sys.argv)
			print usage
			return
		try:
			cutoff = int(sys.argv[2])
			if cutoff <= 0:
				print "cutoff_len be a number greater than 0"
				print " ".join(sys.argv)
				print usage
				return
		except ValueError:
			print "cutoff_len be a number greater than 0"
			print " ".join(sys.argv)
			print usage
			return
			
	# Passed tests #
	
	fafiles = []
	for (dirpath, dirnames, filenames) in os.walk(fadir):
		for f in filenames:
			if f.endswith('.fna') or f.endswith('.fa'):
				fafiles.append(f)
				
	if fadir[-1] == '/':
		fadir = fadir[:-1]
				
	# loaded fasta files #
	
	print ("currently working in ") + os.path.abspath(fadir) + (" with ") + str(len(fafiles)) + (" files")
	sorted_dir = "sorted_" + fadir + "_{0}".format(cutoff)
	try:
		os.mkdir(sorted_dir)
		print "created new directory: " + sorted_dir
	except OSError:
		print "output directory, {0}, already exists".format(sorted_dir)
		cont = raw_input("do you with to continue? (Y/N)")
		if cont != 'Y':
			return
			
	small_fnas = open(sorted_dir + "/small.fna", "w")
	human_fnas = open(sorted_dir + "/human.fna", "w")
	chimp_fnas = open(sorted_dir + "/chimp.fna", "w")
	gorilla_fnas = open(sorted_dir + "/gorilla.fna", "w")
	other_fnas = open(sorted_dir + "/other.fna", "w")
	
	# iterate through fasta files
	seqs = {}
	for fna in fafiles:
		fna_file = open(os.path.abspath(fadir)+"/"+fna)
		
		# iterate through fasta sequences
		for line in fna_file.readlines():
			try:
				if line.strip()[0] == '>':
					seq_id = line.strip()
					seqs[seq_id] = ''
				else:
					seqs[seq_id] += "_" + line.strip()
			except IndexError:
				pass
		fna_file.close()
		
	seq_qty = len(seqs.keys())
	seq_len = [len(seq) for seq in seqs.values()]
	
	# set aside sequence's with len less than cutoff_len
	small_qty = 0
	for key in seqs.keys():
		if len(seqs[key]) - seqs[key].count("_") < cutoff:
			small_qty += 1
			small_fnas.write(key + "\n" + "\n".join(seqs[key].strip("_").split("_")) + "\n")
			del seqs[key]
	small_fnas.close()
	
	# sort remaining seqs by species type
	
	human_len = SpeciesSort(seqs, "human", human_fnas)
	chimp_len = SpeciesSort(seqs, "chimp", chimp_fnas)
	gorilla_len = SpeciesSort(seqs, "gorilla", gorilla_fnas)
	
	for key in seqs.keys():
		other_fnas.write(key + "\n" + "\n".join(seqs[key].strip("_").split("_")) + "\n")
		del seqs[key]
	other_fnas.close
	
	summary = open(sorted_dir + "/summary.txt", "w")
	summary.write("Report:\n"+\
		"Total sequences processed: " + str(seq_qty) + "\n" +\
		"Average sequence length: " + str(Average(seq_len)) + "\n" +\
		"Minimum sequence length: " + str(min(seq_len)) + "\n" +\
		"25% of sequences were smaller than: " + str(np.percentile(seq_len, 25)) + "\n" +\
		"50% of sequences were smaller than: " + str(np.percentile(seq_len, 50)) + "\n" +\
		"75% of sequences were smaller than: " + str(np.percentile(seq_len, 75)) + "\n" +\
		"Maximum sequence length: " + str(max(seq_len)) + "\n" +\
		"Cut off Length: " + str(cutoff) + "\n" +\
		"Number of sub length sequences: " + str(small_qty) +"\n" +\
		"Average passed Sequence length:\n" +\
		"\tHuman\tChimp\tGorilla\n" +\
		"len\t{0}\t{1}\t{2}\n".format(human_len, chimp_len, gorilla_len))
	summary.close()
	print ("Done!")	
	
	
if __name__ == "__main__":
	main()
