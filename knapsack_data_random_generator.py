import random

ITEMS_NUM = 100

weights = []
values = []
for i in range(ITEMS_NUM):
    weights.append(random.uniform(0.1, 10))
    values.append(random.randint(1, 70))

print("weights = ", weights)
print("values = ", values)
print("BAG_SIZE = 50")