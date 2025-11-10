# Служебные утилиты (comm_utils) — логирование, сериализация, контроль соединения.
import datetime

def safe_print(msg):
    """Безопасный вывод с временной меткой"""
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}")
