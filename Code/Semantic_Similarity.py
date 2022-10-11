from scipy import spatial
import pickle
import json


n_candidate_sentences = 5
similarity_threshold = 0.4
n_frequent_techniques = 3

with open("vec/train_dic.DIC", "rb") as f:
    dic_train = pickle.load(f)
with open("vec/test_dic.DIC", "rb") as f:
    dic_test = pickle.load(f)
# with open("vec/dev_dic.DIC", "rb") as f:
#     dic_dev = pickle.load(f)

with open("../data/task1_test.json", "r") as f:
    jsonobj = json.load(f)

with open("../data/task1_train.json", "r") as f:
    jsonobj_train = json.load(f)
dic_tech = {}
for example in jsonobj_train:
    id = example["id"]
    labels = example["labels"]
    dic_tech[id] = labels

with open("../data/task1_dev.json", "r") as f:
    jsonobj_train = json.load(f)

for example in jsonobj_train:
    id = example["id"]
    labels = example["labels"]
    dic_tech[id] = labels


with open("../data/task1_dev_test.json", "r") as f:
    jsonobj_train = json.load(f)
for example in jsonobj_train:
    id = example["id"]
    labels = example["labels"]
    dic_tech[id] = labels

for example in jsonobj:
    techniques_list = []
    target_id = example["id"]
    # arr1 = dic_dev[target_id]
    target_sentence_vec = dic_test[int(target_id)]
    sim = {}
    for key in dic_train:
        sim[key] = spatial.distance.cosine(target_sentence_vec, dic_train[key])
    sort = sorted(sim.items(), key=lambda item: item[1], reverse=True)
    dic_counter = {}
    for i in range(n_candidate_sentences):
        if sort[i][1] < similarity_threshold:    # Only consider those sentences which are more similar then 0.4
            continue
        try:
            list_of_techniques = dic_tech[str(sort[i][0])]
        except KeyError:
            list_of_techniques = dic_tech[sort[i][0]]
        for item in list_of_techniques:
            try:
                dic_counter[item] += 1
            except KeyError:
                dic_counter[item] = 1
    list_temp = sorted(dic_counter.items(), key=lambda item: item[1], reverse=True)
    for i in range(min(n_frequent_techniques, len(list_temp))):
        if list_temp[i][1] < 2:
            continue
        techniques_list.append(list_temp[i][0])
    example['labels'] = techniques_list

task_output_file = "../Submission_Files/output.json"
with open(task_output_file, "w") as f_out:
    json.dump(jsonobj, f_out, indent=4, ensure_ascii=False)
