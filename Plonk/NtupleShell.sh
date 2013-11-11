#!/bin/bash

eval `scram runtime -sh`
printenv
echo $CMSSW_RELEASE_BASE
export LD_LIBRARY_PATH=lib:$LD_LIBRARY_PATH\n
$1
ls -alt