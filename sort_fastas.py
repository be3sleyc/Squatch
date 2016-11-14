#! /usr/bin/env python
## author: Christian Beesley

import sys
import os

def Average(some_list):
    if len(some_list) > 0:
        return sum(some_list) / len(some_list)
    else:
        return 0

def SpeciesSort(ids, species, species_file):
    species_count = []
    species_ids = filter(lambda x:species in x, ids)
    for key in species_ids:
        species_file.write(key + "\n" + "\n".join(seqs[key].strip("_").split("_")) + "\n")
        species_count.append(len("\n".join(seqs[key].strip("_").split("_"))))
        del seqs[key]
    species_file.close()
    return Average(species_count)

usage = 'Usage : sort_fastas.py <cutoff_len>\n\t'+\
    'Sorts through directory containing fasta files and discrimintated by parameter cutoff_len' +\
    'creates a directory: "./sorted_fastas_{n}" where n is the cutoff_len'+\
    '\tdirectory containes fasta files for Gorilla, Chimpanzee, Human, other, and small sequences'+\
    '\tfinishes with a summary of sequences printed to terminal'

if len(sys.argv) == 2:
    if str.isdigit(sys.argv[1]) and int(sys.argv[1]) > 0:
        cutoff_len = int(sys.argv[1])
        cwd = os.getcwd()
        fna_file_qty = [name for name in os.listdir(cwd) if os.path.isfile(name) and name.endswith(".fna")]
        
        #create new dir sorted_fastas
        print ("currently working in ") + cwd + (" with ") + str(len(fna_file_qty)) + (" files\n")
        
        sorted_dir = "sorted_fastas_{0}".format(cutoff_len)
        os.mkdir(sorted_dir)
        small_fnas = open(sorted_dir + "/small.fna", "w")
        human_fnas = open(sorted_dir + "/human.fna", "w")
        chimp_fnas = open(sorted_dir + "/chimp.fna", "w")
        gorilla_fnas = open(sorted_dir + "/gorilla.fna", "w")
        other_fnas = open(sorted_dir + "/other.fna", "w")
        
        # iterate through fasta files
        seqs = {}
        for fna in fna_file_qty:
            fna_file = open(fna)
            
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
        
        # set aside sequence's  with len less than cutoff_len
        small_qty = 0
        for key in seqs.keys():
            if len(seqs[key]) - seqs[key].count("_") < cutoff_len:
                small_qty += 1
                small_fnas.write(key + "\n" + "\n".join(seqs[key].strip("_").split("_")) + "\n")
                del seqs[key]
        small_fnas.close()
        
        # sort remaining seqs by species type
        
        seq_ids = seqs.keys()
        
        human_len = SpeciesSort(seq_ids, "human", human_fnas)
        chimp_len = SpeciesSort(seq_ids, "chimp", chimp_fnas)
        gorilla_len = SpeciesSort(seq_ids, "gorilla", gorilla_fnas)
        
        for key in seqs.keys():
            other_fnas.write(key + "\n" + "\n".join(seqs[key].strip("_").split("_")) + "\n")
            del seqs[key]
        other_fnas.close
        
	summary = open(sorted_dir + "/summary.txt", "w")
        summary.write("Report:\n"+\
            "Total sequences processed: " + str(seq_qty) + "\n" +\
            "Number of sub length sequences: " + str(small_qty) +"\n" +\
            "Average Sequence length:\n" +\
            "\tHuman\tChimp\tGorilla\n" +\
            "len\t{0}\t{1}\t{2}\n".format(human_len, chimp_len, gorilla_len))
        print ("Done!")
    else:
        print ("cutoff_len must be a number greater than 0")
        print (usage)
else:
    print(usage)

