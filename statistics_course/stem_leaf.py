data = \
[87, 51, 56, 59, 90, 67, 74, 96, 73, 80,
 92, 68, 92, 79, 95, 68, 87, 93, 91, 80,
 65, 92, 77, 94, 89, 74, 96, 85, 93, 72,
 49, 79, 65, 62, 70, 76, 87, 74, 63, 94,
 86, 86, 69, 88, 89, 97, 91, 54, 83, 73]

sorted_data = sorted(data)

stem_lef = {}
temp = []
keys = []

for num in sorted_data:
    key = num // 10
    value = num % 10
    if key not in keys:
        keys.append(key)
        temp.clear()
        temp.append(value)
        new_list = temp.copy()
        stem_lef[key] = new_list
    else:
        temp.append(value)
        new_list = temp.copy()
        stem_lef[key] = new_list
print(stem_lef)









