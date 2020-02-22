#!/bin/bash

# SDK TEMPLATE by D_Skywalk

## SDK PATH
export DAADDEV=/your/path/to/devkit
export PATH=$PATH:$DAADDEV/bin

## DAADLIB
export DAAD_LIB_PATH=$DAADDEV/lib
export PS1='\[\e[1;31m\]\W/ ~ [DAAD] \$\[\e[0m\] '

echo 
echo DAAD devkit by SKY
echo ------------------------
echo Path Loading!
echo on $DAADDEV
echo 

