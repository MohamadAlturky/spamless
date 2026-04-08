@echo off
setlocal

set PYTHON=C:\Users\ASUS\AppData\Local\Programs\Python\Python313\python.exe
set VENV=.venv

:: Create virtual environment if it doesn't exist
if not exist %VENV% (
    echo Creating virtual environment...
    %PYTHON% -m venv %VENV%
)

:: Activate virtual environment
echo Activating virtual environment...
call %VENV%\Scripts\activate.bat

:: Install dependencies from requirements.txt
echo Installing dependencies...
pip install -r requirements.txt --quiet

:: Set PYTHONPATH so PyInstaller can find src/spamless
set PYTHONPATH=src

echo Building exe...
pyinstaller ^
  --onefile ^
  --name spamless ^
  --console ^
  --distpath dist ^
  --workpath build ^
  --specpath . ^
  src\spamless\__main__.py

:: Copy .env alongside the exe so it can find the API keys at runtime
echo Copying .env to dist\...
copy .env dist\.env >nul

echo.
echo Done! Executable is at: dist\spamless.exe
endlocal
