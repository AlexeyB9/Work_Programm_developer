@echo off
echo Запуск проекта локально (Windows)...
echo.

REM Проверка виртуального окружения
if exist venv\Scripts\activate.bat (
    echo Активация виртуального окружения...
    call venv\Scripts\activate.bat
) else (
    echo Создание виртуального окружения...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Установка зависимостей...
    pip install -r requirements.txt
)

REM Проверка переменных окружения
if "%PPLX_API_KEY%"=="" (
    echo.
    echo ВНИМАНИЕ: PPLX_API_KEY не установлен!
    echo Установите: set PPLX_API_KEY=ваш_ключ
    echo.
)

echo.
echo Запуск всех сервисов...
python run_all.py

pause

