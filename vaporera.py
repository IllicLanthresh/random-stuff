from collections import defaultdict

food_len = int(input("Cuantos alimentos hay? "))
food_list = list()
for _ in range(food_len):
    food_list.append({"name": input("introduce nombre del alimento: "),
                      "time": int(input("introduce tiempo de cocción: "))})

food_list.sort(key=lambda a: a["time"], reverse=True)

max_time = food_list[0]["time"]

cooking_order = defaultdict(list)
for el in food_list:
    cooking_order[max_time-el["time"]].append(el["name"])

for min, names in cooking_order.items():
    print("min ", min, " : ", ", ".join(names))
