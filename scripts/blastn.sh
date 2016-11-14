#! /bin/bash
# $1=fna containing directory
# $2=desired database to blast against
# $3=evalue

y=$2_$3_blast
if [ ! -d "$1/$2_blast" ]; then
	mkdir $1/$y
	echo created $y directory
fi

for f in $1/*.fna ;
do
	echo blasting $f against $2 database
	x=${f%.fna}.blast
	z=${x##*/}
	blastn -db $BLASTDB/$2 -query $f -evalue $3 >$1/$y/$z
done
