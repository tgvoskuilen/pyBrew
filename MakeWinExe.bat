python C:\Users\Tyler\Downloads\PyInstaller-2.1\PyInstaller-2.1\pyinstaller.py --onefile --noconsole -i icons/pyBrew.ico pyBrew.py
move /Y dist\pyBrew.exe .
"C:\Program Files (x86)\NSIS\makensis" ConfigureInstaller.nsi
rmdir /s /q build
rmdir /s /q dist
del pyBrew.exe
del pyBrew.spec
move /Y pyBrewInstaller.exe installers