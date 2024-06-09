#!/bin/bash

clear
cd machine || exit

echo "Removing environment..."
if [ -d ".venv" ]; then
    rm -rf .venv
fi

echo "Removing storage..."
if [ -d "disks" ]; then
    rm -rf disks
fi

cd ..

read -p "Setup the machine again ? (Y/N)" answer

if [ "$answer" = "Y" ] || [ "$answer" = "y" ]; then
    ./cmd/update.sh
    ./cmd/setup.sh
else
    echo "The machine has been reset to its primary state."
fi