# Базовая запись логов
def log_data(data):
    with open("central_node/log.txt", "a") as f:
        f.write(str(data) + "\n")
    print("Данные записаны в лог")
