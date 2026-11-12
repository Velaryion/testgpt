@echo off
setlocal
cd /d "%~dp0"
py -3.12 -m venv .venv
if errorlevel 1 goto error
.venv\Scripts\python -m pip install -r requirements-windows.txt
if errorlevel 1 goto error
.venv\Scripts\python -m unittest discover -s tests -v
if errorlevel 1 goto error
.venv\Scripts\python -m PyInstaller --noconfirm --clean --onefile --windowed --collect-all webview --name AnimeDesk app.py
if errorlevel 1 goto error
start "" /wait "dist\AnimeDesk.exe" --smoke-test
if errorlevel 1 goto error
start "" /wait "dist\AnimeDesk.exe" --browser-smoke-test
if errorlevel 1 goto error
echo EXE creado en %CD%\dist\AnimeDesk.exe
explorer "%CD%\dist"
pause
exit /b 0
:error
echo No se ha completado la compilacion. Revisa el error anterior.
echo Necesitas Python 3.12 para Windows, incluido el lanzador py.
pause
exit /b 1
