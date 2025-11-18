# Script to create executable
import PyInstaller.__main__

PyInstaller.__main__.run([
    'EscapeOfTheNightmare.py',
    '--windowed',
    '--console', # --noconsole for MacOs
    '--onefile',
    '--icon=./assets/icon.png',
    '--distpath=./executable_output',
    '--workpath=./executable_work_dir',
    '--add-data=assets:assets'

])