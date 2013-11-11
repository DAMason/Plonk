#!/bin/bash

eval `scram runtime -sh`
printenv
echo $CMSSW_RELEASE_BASE
cmsRun $1
ls -alt

