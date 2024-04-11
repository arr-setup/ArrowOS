clear
cd machine || exit

echo "Removing environment..."
rm -rf .venv
echo "Removing storage..."
rm -rf disks

cd ..

read -p "Setup the machine again ? (Y/N)" answer

if [ "$answer" = "Y" ] || [ "$answer" = "y" ]; then
    ./cmd/update
    ./cmd/setup
else
    echo "The machine has been reset to its primary state."
fi