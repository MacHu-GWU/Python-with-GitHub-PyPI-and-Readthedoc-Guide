pushd "%~dp0"
cd canbeAny
python zzz_manual_install.py
cd ..
python create_doctree.py
make html