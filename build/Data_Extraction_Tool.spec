# -*- mode: python ; coding: utf-8 -*-

add_files = [(r'Assets\*.png', 'Assets'),
             (r'PDF\Data Extraction Tool User Guide R0.pdf', 'PDF'),
             (r'Assets\*.ico', 'Assets'),
             (r'EULA\EULA.txt', 'EULA')]

block_cipher = None


a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=add_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

splash = Splash(
    r'Assets\Splash_image.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=(10, 195),
    text_size=12,
    text_color='black',
    text_default='Loading...',
    minify_script=True,
    always_on_top=True,
)

exe = EXE(pyz,
          splash,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Data_Extraction_Tool',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon=r'Assets\Icon.ico',
          disable_windowed_traceback=False,
          argv_emulation=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          version='version_file.txt')
coll = COLLECT(exe,
               splash.binaries,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Data_Extraction_Tool')
