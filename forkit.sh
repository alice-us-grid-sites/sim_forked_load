#!/bin/bash

pwd

ls -l
ls -ld .

cd sim_forked_load
echo "after cd sim_forked_load"


pwd
ls -l
ls -ld ../

cmd="time ./forkit.py "

echo $cmd
sleep 30

$cmd

