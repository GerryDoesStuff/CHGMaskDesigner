@echo off
setlocal

REM Change to the directory containing this script
cd /d "%~dp0"

REM Ensure a virtual environment exists
if not exist .venv (
    echo [CGH Mask Designer] Creating virtual environment in .venv
    python -m venv .venv
    if errorlevel 1 goto :error
)

REM Activate the virtual environment
call .venv\Scripts\activate
if errorlevel 1 goto :error

REM Upgrade pip to the latest version
python -m pip install --upgrade pip
if errorlevel 1 goto :error

REM Install the CGH Mask Designer package into the virtual environment
python -m pip install .
if errorlevel 1 goto :error

REM Launch the application
python -m cgh_mask_designer
if errorlevel 1 goto :error

goto :end

:error
echo.
echo [CGH Mask Designer] An error occurred. See messages above for details.

:end
echo.
pause
