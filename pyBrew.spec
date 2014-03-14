# -*- mode: python -*-
a = Analysis(['pyBrew.py'],
             pathex=['C:\\Users\\Tyler\\Dropbox\\Programs\\pyBrew'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pyBrew.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
