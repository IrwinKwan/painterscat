# -*- mode: python -*-
a = Analysis(['painterscat.py'],
             pathex=['C:\\Users\\Administrator\\Documents\\painterscat'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          Tree('data', prefix='data'),
          name=os.path.join('dist', 'painterscat.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False )
