def visualize(intersection_id, state):
    # Простая текстовая визуализация состояния светофора
    bar = {"RED": "🔴", "YELLOW": "🟡", "GREEN": "🟢"}
    print(f"[{intersection_id}] Светофор: {bar.get(state, state)}")
