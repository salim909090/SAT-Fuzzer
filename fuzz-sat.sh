#!/bin/bash

sut_path=$1
input_path=$2

#pip3 install -r requirements.txt

python3 fuzzer.py $1 $2 --seed 1234567