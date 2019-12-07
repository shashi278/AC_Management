# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

from kivy.deps import sdl2, glew
path=os.path.abspath(".")
a = Analysis(['src\\main.py'],
             pathex=[path],
             binaries=[],
             datas=[("src\\*.kv","."),("src\\*.py","."),("src\\animator\\*","animator\\"),("src\\media\\images\\*","media\\images"),("src\\*.sql",".")],
             hiddenimports=["kivymd.uix.card",'win32timezone'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['cv2'],
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
          icon='src\\media\\images\\app_icon.ico',
          console=False )   ##True if console needed
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='Account management System')
