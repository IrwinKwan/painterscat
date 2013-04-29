# -*- mode: python -*-
a = Analysis(['painterscat.py'],
             pathex=['/Users/kwan/Development/painterscat'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.darwin/painterscat', 'painterscat'),
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'painterscat'))
app = BUNDLE(coll,
             Tree('data', prefix='data'),
             name=os.path.join('dist', 'painterscat.app'))
