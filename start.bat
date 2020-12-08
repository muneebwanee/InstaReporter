@echo off
python -V >nul 2>&1 && (
    python InstaReporter.py
) || (
    echo "Python 3.7 not found, please install Python!"
    timeout /t 5 /nobreak > NUL
    exit
)

timeout /t 15 /nobreak > NUL