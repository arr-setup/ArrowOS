#!/bin/bash

clear
cd machine || exit

echo "Welcome to ArrowBit !"
source .venv/scripts/activate
echo "..."
python -m main

cd ..