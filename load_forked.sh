#!/bin/bash

pwd

ls -l
ls -ld .

cd sim_forked_load
echo "after cd sim_forked_load"

pwd
ls -l
ls -ld ../

cmd="time ./load_forked.py -$1"

echo $cmd

$cmd

