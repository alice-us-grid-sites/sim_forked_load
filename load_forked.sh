#!/bin/bash

pwd

cd sim_forked_load

cmd="time ./load_forked.py -$1"

echo $cmd

$cmd

