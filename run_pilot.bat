@echo off
title Пилот raкhsh — полный симулятор

rem --- Окно для traffic_light
start cmd /k "python controllers\traffic_light.py"

rem --- Окно для sensor_interface
start cmd /k "python controllers\sensor_interface.py"

rem --- Окно для network_comm
start cmd /k "python controllers\network_comm.py"

rem --- Окно для центрального узла ЦУАК
start cmd /k "python central_node\main.py"

rem --- Окно для симулятора с визуализацией
start cmd /k "python simulator\simulate_intersection.py"

echo Пилот raкhsh запущен полностью.
pause
