#!/bin/bash

if [[ !($# -eq 2) ]]; then
	echo "Usage : $0 dossier label"
else
	directory=$1
	label=$2

	cd $directory

	for f in `ls`
	do
		echo -e "label : $label;\ntexte : " | cat - $f > temp && mv temp $f && echo "$f labellisé"
	done
fi
