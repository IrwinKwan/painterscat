# -*- mode: python -*-
a = Analysis(['painterscat.py'],
             pathex=['/Users/kwan/Development/painterscat'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'painterscat'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
