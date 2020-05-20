#!/bin/bash

cmd="time ./load_forked.py -$1"

echo $cmd

$cmd

