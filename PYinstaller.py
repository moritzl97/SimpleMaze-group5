
import PyInstaller.__main__

PyInstaller.__main__.run([
    'EscapeOfTheNightmare.py',
    '--windowed',
    '--console', # --noconsole for MacOs
    '--onefile',
    '--icon=./assets/icon.png',
    '--distpath=./output',
    '--workpath=./working',
    '--add-data=assets:assets'

])