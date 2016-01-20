pushd "%~dp0"
python setup.py sdist
python setup.py build --plat-name=win32 bdist_wininst
python setup.py build --plat-name=win-amd64 bdist_wininst
pause