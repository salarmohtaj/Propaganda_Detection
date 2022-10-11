

import sys
import json
import random
import argparse
import warnings


random.seed(42) # to make runs deterministic


def baseline(propaganda_techniques_file, dev_file, task_output_file):
    try:
        with open(dev_file, "r") as f:
            jsonobj = json.load(f)
    except:
        sys.exit("ERROR: cannot load json file")

    with open(propaganda_techniques_file, "r") as f:
        propaganda_techniques_names = [ line.rstrip() for line in f.readlines() if len(line)>2 ]

    for example in jsonobj:

        techniques_list = []
        i = 0
        tmp_propaganda_techniques_names = propaganda_techniques_names[:]
        while i < len(propaganda_techniques_names) and random.random() < 0.5:
            random_technique = tmp_propaganda_techniques_names[random.randint(0, len(tmp_propaganda_techniques_names)-1)]
            techniques_list.append(random_technique)
            # tmp_propaganda_techniques_names.remove(random_technique)
            i += 1

        if(len(techniques_list)==0):
            random_technique = propaganda_techniques_names[random.randint(0, len(propaganda_techniques_names) - 1)]
            techniques_list.append(random_technique)
            i += 1

        example['labels'] = techniques_list
        print("example %s: added %d labels" % (example['id'], i))

    with open(task_output_file, "w") as fout:
        json.dump(jsonobj, fout, indent=4,ensure_ascii=False)
    print("Predictions written to file " + task_output_file)


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    parser = argparse.ArgumentParser()
    parser.add_argument('--in-file', type=str)
    parser.add_argument('--out-file', type=str)

    args = parser.parse_args()


    dev_file = args.in_file
    task_output_file=args.out_file
    propaganda_techniques_file = "./techniques_list_task1-2.txt"

    baseline(propaganda_techniques_file, dev_file, task_output_file)