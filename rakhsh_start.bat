@echo off
REM ===== Rakhsh-Dushanbe: запуск всех процессов =====
echo Запуск Mosquitto...
net start mosquitto

echo Запуск центрального узла (main.py)...
start cmd /k python central_node/main.py

echo Запуск AI оптимизатора...
start cmd /k python core/ai_optimizer.py

echo Запуск веб-сервера...
start cmd /k python ui/web_server.py

echo Все процессы запущены.
pause
