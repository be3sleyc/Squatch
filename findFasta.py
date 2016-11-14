#! /usr/bin/env python
## author: Christian Beesley

import sys
import re
from Bio import SeqIO

usage = 'This script assembles a fasta file of all the squences in a blast output file '\
        '\tUsage: ./findFasta.py <blast_file> <fasta_file>'

if len(sys.argv) < 3:
    print usage
    sys.exit(0)
else:
    blastf = sys.argv[1]
    print 'blast output file:', sys.argv[1]
    fastr = sys.argv[2]
    print 'reference fasta file:', sys.argv[2]

outfile = sys.argv[1] + '.fna'

with open(blastf) as infile:
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
    blastids += result.group(1)
    blastids += '\n'

blastids = blastids.strip()
#print blastids
#print '\n'

fastas = [seq for seq in SeqIO.parse(fastr, "fasta")]
#for fasta in fastas:
    #print fasta.id

of = open(outfile, 'w')
for id in blastids.split('\n'):
    for f in fastas:
        if id == f.id:
            SeqIO.write(f, of, "fasta")
of.close()

