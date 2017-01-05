#! /usr/bin/env python
## author: Christian Beesley

import sys
import os
import re
from Bio import SeqIO

usage = "Usage: ./findFasta.py <blast_dir> <fasta_dir>\n"+\
	"\t This script assembles a fasta file of all the squences in a blast output file\n" +\
	"\t It takes a directory containing blast outputs and a directory containing\n" +\
	"\t fasta files used in the blast searches."

def findFasta(specimen, blast_file, fasta_file, out_dir):
	
	outfile = out_dir + "/" + specimen + '.fna'
	with open(blast_file) as infile:
		blastfile = ''
		temp = ''
		add = False
		for line in infile.readlines():
			if add:
				if line[0:6] != 'Length':
					temp += line.strip()
				else:
					add = False
			if line[0:6] == 'Query=':
				temp += line.strip()[7:]
				add = True
			elif line[0:6] == '***** ':
				temp = ''
			elif line[0:6] == 'Sequen':
				blastfile += temp
				blastfile += '\n'
				temp = ''

	blastfile = blastfile.strip()
	blastids = ''
	for line in blastfile.split('\n'):
		result = re.search('(.*\.\d+)\s*\d\d\w/\d\d\w.*', line)
		try:
			blastids += result.group(1)
			blastids += '\n'
		except (AttributeError):
			pass

	blastids = blastids.strip()

	fastas = [seq for seq in SeqIO.parse(fasta_file, "fasta")]

	of = open(outfile, 'w')
	for id in blastids.split('\n'):
		for f in fastas:
			if id == f.id:
				SeqIO.write(f, of, "fasta")
				
	of.seek(0, os.SEEK_END)
	size = of.tell()
	of.close()
	if size == 0:
		os.remove(of.name)

def main():
	if len(sys.argv) != 3:
		print "be sure to include all parameters"
		print usage
		return
	elif not os.path.isdir(sys.argv[1]) or not os.path.isdir(sys.argv[2]):
		print "please include valid directories"
		print usage
		return
	else:
		blastd = sys.argv[1]
		if blastd.endswith('/'):
			blastd = blastd[:-1]
		print 'blast output directory:', blastd
		fastd = sys.argv[2]
		if fastd.endswith('/'):
			fastd = fastd[:-1]
		print 'reference fasta directory:', fastd
		
	#passed tessts

	species_seqs = {}
	for (dirpath, dirnames, filenames) in os.walk(fastd):
		for f in filenames:
			if f.endswith('.fna'):
				key = f.split('.')[0]
				species_seqs[key] = [f]
	for (dirpath, dirnames, filesnames) in os.walk(blastd):
		for b in filesnames:
			key = b.split('_')[0]
			species_seqs[key].append(b)
	
	try:
		out_dir = "Found_"+ fastd
		os.mkdir(out_dir)
		print "created new directory: " + out_dir
	except OSError:
		print "Output directory, {0}, already exists".format(out_dir)
		cont = raw_input("Do you with to continue? (Y/N)")
		if cont != 'Y':
			return

	for key,v in species_seqs.items():
		blast_file = blastd+"/"+v[1]
		fasta_file = fastd+"/"+v[0]
		print "searching for matching fasta files in " + fasta_file + " and " + blast_file
		findFasta(key, blast_file, fasta_file, out_dir)
	print "Done!"
		
if __name__ == '__main__':
	main()
