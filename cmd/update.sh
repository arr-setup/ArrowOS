clear
cd machine || exit

rm -rf .venv

echo "Setting a new venv..."
python3 -m venv .venv
source .venv/bin/activate

echo "Upgrading pip..."
python -m pip install -q --upgrade pip

echo "Installing modules..."
python -m pip install -q adrv cryptography requests bcrypt

cd ..