@echo off

REM Ativa o ambiente virtual
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting API server...
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
