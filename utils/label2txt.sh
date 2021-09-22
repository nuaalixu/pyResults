#!/bin/bash
if [[ $# != 1 ]];then
	echo "$0"
	echo "原始标注mlf文件转txt文件"
	echo "Usage: $0 <raw-mlf>"
	echo "e.g.: $0 chn_niuman_191210.all.mlf"
	exit 1
fi

cat $1 | egrep -v 'invalid|sil' | sed -E 's/\([0-9a-zA-Z]+\)//g;s/[（）()]//g;s/null//g' | perl -e 'while(<>){chomp;$out=$_;if($_=~m/"\*\/(.*)\.lab"/){print $1." ";}elsif($_=~m/^(\d+)\s+(\d+)\s*(.*)$/){$text=uc($3);$out="$text";print "$out"}elsif($_=~m/^\.$/){print "\n"}}' |awk '{if(NF==1)$0=$0" NULL";print $0}'
