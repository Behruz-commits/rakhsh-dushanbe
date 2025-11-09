# Простейший ИИ-оптимизатор светофорного цикла
def optimize_cycle(data):
    vehicles = data["vehicles"]
    pedestrians = data["pedestrians"]
    if vehicles > 10:
        print("Увеличиваем время зеленого для машин")
    if pedestrians > 5:
        print("Увеличиваем время зеленого для пешеходов")
