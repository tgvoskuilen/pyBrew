REM python C:\Users\Tyler\Downloads\PyInstaller-2.1\PyInstaller-2.1\pyinstaller.py --onefile pyBrew.py^
python C:\Users\Tyler\Downloads\PyInstaller-2.1\PyInstaller-2.1\pyinstaller.py pyBrew.spec
move /Y dist\pyBrew.exe .
"C:\Program Files (x86)\NSIS\makensis" ConfigureInstaller.nsi
rmdir /s /q build
rmdir /s /q dist
del pyBrew.exe
move /Y pyBrewInstaller.exe installers