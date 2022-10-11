import pickle
dic_techniques = {}

i = 0
with open("../techniques_list_task1-2.txt", 'r') as f:
    for line in f:
        name = line.strip()
        dic_techniques[name] = i
        i += 1

print(dic_techniques)
with open("techniques.DICT", "wb") as f:
    pickle.dump(dic_techniques, f)
