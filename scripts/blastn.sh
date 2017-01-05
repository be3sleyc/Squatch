#! /bin/bash
# $1=fna containing directory
# $2=desired database to blast against
# $3=evalue

# remove "/" from end of input directory if present
regex="(.+)/"

if [[ $1 =~ $regex ]]; then
	fna="${BASH_REMATCH[1]}"
fi

#define and create the output directory
IFS='_' read -r -a array <<< "$fna"
regex2="\d+"
c=$(echo )
for portion in ${array[@]}
do
	if [[ portion =~ $regex2 ]]; then
		c=$c$(echo $portion)
	else
		c=$c$(echo $portion | head -c 4)
	fi
done

x=$c$2_blast_$3
if [ ! -d "$x" ]; then
	mkdir $x
	echo created $x directory
fi

#blast the fasta files and store in output directory
for f in $fna/*.fna ;
do
	echo -e '\t' blasting $f against $2 database
	#create output blast file
	z=$x/$(basename ${f%.fna})_$3.blast
	#blast
	blastn -db $BLASTDB/$2 -query $f -evalue $3 -num_threads 2 -culling_limit 25 >$z
done

echo Done!
