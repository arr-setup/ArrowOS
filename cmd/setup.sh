clear
cd machine || exit

if [ -d ".venv" ]; then
    read -p "Remove the existing venv ? (Y/N - Recommended if you want an up-to-date machine) " answer

    if [ "$answer" = "Y" ] || [ "$answer" = "y" ]; then
        cd ..
        ./cmd/update
        cd machine || exit
    else
        echo "The venv has been conserved. Please setup the machine again before submitting a bug report if you have a problem"
        source .venv/scripts/activate
    fi
else
    echo "Setting venv..."
    python3 -m venv .venv
    source .venv/bin/activate

    echo "Installing modules..."
    python -m pip install -q --upgrade pip
    python -m pip install -q adrv cryptography requests bcrypt
fi

echo "Starting machine..."
python -m setup
python -m main

cd ..