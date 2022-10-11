import pandas as pd
import json
import pickle


with open("../data/task1_test.json", 'r') as f:
    data = json.load(f)

with open("techniques.DICT", "rb") as f:
    tech_dict = pickle.load(f)


# df = pd.DataFrame(columns=['id','text','label'])
df = pd.DataFrame(columns=['id','text'])
print(len(data))
for index, item in enumerate(data):
    # label_list = [0] * 21
    # labels = item["labels"]
    # for label in labels:
    #     label_list[tech_dict[label]] = 1
    # df.loc[index] = pd.Series({'id':item['id'], "text":item["text"], "label":label_list})
    df.loc[index] = pd.Series({'id': item['id'], "text": item["text"]})
print(df.head())
df.to_csv("../data/task1_test.tsv", sep="\t", index=False)