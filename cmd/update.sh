#!/bin/bash

clear
cd machine || exit

rm -rf .venv

echo "Setting a new venv..."
python -m venv .venv
source .venv/scripts/activate

echo "Upgrading pip..."
python -m pip install -q --upgrade pip

echo "Installing modules..."
python -m pip install -q adrv cryptography requests bcrypt

cd ..