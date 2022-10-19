import json
import matplotlib.pyplot as plt

with open("../data/task1_train.json", "r") as f:
    train = json.load(f)

print(len(train))
train_word = []
for item in train:
    train_word.extend(item["text"].split(" "))
    # train_word.append(len(item["text"].split(" ")))

print(len(train_word))
print(len(set(train_word)))

with open("../data/task1_test.json", "r") as f:
    test = json.load(f)

test_word = []
test_len = []
id = {}
for item in test:
    try:
        r = id[item["id"]]
    except:
        id[item["id"]] = 1
        n_words = item["text"].split(" ")
        test_len.append(len(n_words))
        test_word.extend(n_words)


print(len(test_word))
print(len(set(test_word)))
print(min(test_len))
print(max(test_len))
print(sum(test_len)/len(test_len))

tech = {}
for item in train:
    list_of_techniques = item["labels"]
    for i in list_of_techniques:
        try:
            tech[i] += 1
        except KeyError:
            tech[i] = 1
print(tech)
sorted_list = sorted(tech, key=tech.get, reverse=True)
dic = {}

for index, item in enumerate(sorted_list):
    if index < 8:
        dic[item] = tech[item]
    else:
        try:
            dic["others"] += tech[item]
        except KeyError:
            dic["others"] = 0

print(dic)

import matplotlib as mpl
mpl.rcParams['xtick.labelsize'] = 13
color_1 = "darkorange"
color_2 = "royalblue"
fig = plt.figure()

color_list = [color_2] * 8
color_list.append(color_1)

plt.bar(range(len(dic)), list(dic.values()), align='center', color=color_list, edgecolor = color_2)
plt.xticks(range(len(dic)), list(dic.keys()), rotation=90)
plt.tight_layout()
plt.savefig("img/tech_distribution.pdf", format='pdf')
plt.show()

