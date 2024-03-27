#!/bin/bash

echo "MAKE SURE TO NOT HAVE ANYTHING IN THE ./dist DIRECTORY"
echo "Continue? (Y/N)"
read user_input

if [ "$user_input" == "y" ] || [ "$user_input" == "Y" ]; then
    echo ""
else
    echo "Exiting..."
    exit
fi

rm Jotabot.spec
rm -rf ./build
mv ./dist/Jotabot ./Jotabot
rm -rf ./dist

python3 --version
pyinstaller --version
pyinstaller main.py --name Jotabot --onefile --icon ./icon.png

rm Jotabot.spec
rm -rf ./build
mv ./dist/Jotabot ./Jotabot
rm -rf ./dist
