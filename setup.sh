#!/bin/sh

mkdir raspiMacedoPIF

cd raspiMacedoPIF

git clone git://github.com/stevenmacedo/pifdc3if

chmod 1777 pifdc3if

cd pifdc3if

pip install -r requirements.txt

python app.py

