@echo off
setlocal

rem Navigate to the project directory (relative to this script)
pushd "%~dp0kolofortuny" || (
  echo Project directory not found: "%~dp0kolofortuny"
  pause
  exit /b 1
)

rem Activate the virtual environment
if exist "kolovenv\Scripts\activate.bat" (
  call "kolovenv\Scripts\activate.bat"
) else (
  echo Virtual environment activation script not found: kolovenv\Scripts\activate.bat
  popd
  pause
  exit /b 1
)

rem Launch the Streamlit application (forward any arguments)
python -m streamlit run app.py %*

rem Return to the original directory
popd
endlocal