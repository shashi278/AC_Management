# -*- mode: python ; coding: utf-8 -*-

#Specification file to generate an exe

#to build, run `pyinstaller pyinstaller.spec`
#Built exe will be in `dist` folder

block_cipher = None

from kivy.deps import sdl2, glew
path=os.path.abspath(".")
a = Analysis(['src\\main.py'],
             pathex=[path],
             binaries=[],
             datas=[("src\\*.kv","."),("src\\*.py","."),("src\\animator\\*","animator\\"),("src\\media\\images\\*","media\\images"),("src\\*.sql",".")],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Account Management System',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )   ##True if console needed
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='Account management System')
