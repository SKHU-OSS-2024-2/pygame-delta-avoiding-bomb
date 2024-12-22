# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['bomb_game\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('bomb_game/font/*', 'bomb_game/font'), ('bomb_game/sound/*', 'bomb_game/sound'), ('bomb_game/img/*', 'bomb_game/img'), ('bomb_game/font/Pixelify_Sans/static/Pixelifysans-Medium.ttf', 'bomb_game/font/Pixelify_Sans/static'), ('bomb_game/img/bomb.png', 'bomb_game/img')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
