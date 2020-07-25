#!/bin/bash
files=(lit101 lit301 p101 mv101 p301 plant plc1 plc2 plc3 controller)
rm -rf output/*
for file in "${files[@]}"
do
      touch output/$file".log"
done
