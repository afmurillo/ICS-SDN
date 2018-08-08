#!/bin/bash

echo "Limpiando archivo" $1
sed -e '1,3d' $1 > aux.txt
replace "[" "" -- aux.txt
replace "]" "" -- aux.txt
replace "," "" -- aux.txt
sed -i '$ d' aux.txt
cat aux.txt > $1


