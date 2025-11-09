# Центральный узел адаптивного контроля (ЦУАК)
from central_node.data_collector import collect_data
from central_node.ai_optimizer import optimize_cycle

def main():
    print("ЦУАК запущен")
    while True:
        data = collect_data()
        optimize_cycle(data)

if __name__ == "__main__":
    main()
