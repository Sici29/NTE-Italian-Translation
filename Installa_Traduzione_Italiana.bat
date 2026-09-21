@echo off
setlocal
cd /d "%~dp0"

if exist "NTE-Italian-Translation.exe" (
  "NTE-Italian-Translation.exe" install %*
  pause
  exit /b %ERRORLEVEL%
)

if exist "tools\nte_it_installer.py" (
  python "tools\nte_it_installer.py" install %*
  pause
  exit /b %ERRORLEVEL%
)

echo [ERRORE] Eseguibile o script di installazione non trovato!
pause
exit /b 1
