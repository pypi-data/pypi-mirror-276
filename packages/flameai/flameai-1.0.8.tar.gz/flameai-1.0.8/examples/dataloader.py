from flameai.preprocessing import DataLoader

dt = DataLoader([1, 2, 3, 4, 5])
for i in dt:
    print(i)
for i in dt:
    print(i)

dt.data = [1, 2, 3]
print([e for e in dt])
