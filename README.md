# Data for Propaganda Detection in Arabic shared task at WANLP!

The website of the shared task, with the submission instructions, updates on the competition and the live leaderboard can be found here: https://sites.google.com/view/propaganda-detection-in-arabic/

__Table of contents:__

- [Dataset](#wanlp2022-propaganda-in-arabic-corpus)
  - [List of Versions](#list-of-versions)
  - [Task Description](#task-description)
  - [Data Format](#data-format)
  - [Format checkers](#format-checkers)
  - [Scorers](#scorers)
  - [Baseline](#baseline)
  - [Licensing](#licensing)
  - [Citation](#citation)
- [Additional Resources](#additional-resources)
- [Recommended reading](#recommended-reading)

## List of Versions
* [2022/09/11]__ - Released test data
* [2022/07/23]__ - Updated train, dev, and dev-test data for task 1 and train data for task 2
* [2022/07/23]__ - Train, dev, and dev-test data released for task 1 and 2

 Note that, for both subtasks, you are free to use the annotations of the [PTC corpus](https://propaganda.qcri.org/semeval2020-task11/) (more than 20,000 sentences). The PTC corpus contains news articles in English, but the annotations are made using the same guidelines, but using 18 instead of 20 propaganda techniques. The dataset can be used either in a translated version or using multilingual representations. 

## Task Description

**Subtask 1:** Given the text of a tweet, identify the propaganda techniques used in it (multilabel classification problem).

**Subtask 2:** Given the text of a tweet, identify the propaganda techniques used in it together with the span(s) of text in which each propaganda technique appears.


## Data Format

All datasets are JSON files. The text encoding is UTF-8. The data is located in:
* **Subtask 1:**
  * data/task1_train.json
  * data/task1_dev.json
  * data/task1_dev_test.json 
  * data/task1_test.json (test set for task 1)
* **Subtask 2:**
  * data/task2_train.json
  * data/task2_dev.json
  * data/task2_dev_test.json
  * data/task2_test.json (test set for task 2)


**Note:** The input and the result files have the same format for all the subtasks.

### Input data format

#### Subtask 1:
An object of the JSON has the following format:
```
{
  id -> identifier of the example,
  labels -> the list of propaganda techniques appearing in the text,
  text -> text
}
```
##### Example
```
    {
        "id": "1389927866356412416",
        "text": "\"ده مش معتقل ده أحسن من اللوكاندة\".. جدل وسخرية من زيارات تنظمها وزارة الداخلية للسجون #مصر https://t.co/VkkCrRjOCF",
        "labels": [
            "Exaggeration/Minimisation",
            "Smears"
        ]
    }
```
#### Subtask 2:
An object of the JSON has the following format:
```
{
  id -> identifier of the example,
  text -> text
  labels : [ -> list of objects
    {
      start -> start index of the span covering the technique,
      end -> end index of the span covering technique,
      technique -> technique in the given span,
      text_fragment -> textual content of the span
    }
  ]
}
```
##### Example
```
{
        "id": "1389927866356412416",
        "text": "\"ده مش معتقل ده أحسن من اللوكاندة\".. جدل وسخرية من زيارات تنظمها وزارة الداخلية للسجون #مصر https://t.co/VkkCrRjOCF",
        "labels": [
            {
                "start": 1,
                "end": 33,
                "technique": "Exaggeration/Minimisation",
                "text": "ده مش معتقل ده أحسن من اللوكاندة"
            },
            {
                "start": 37,
                "end": 86,
                "technique": "Smears",
                "text": "جدل وسخرية من زيارات تنظمها وزارة الداخلية للسجون"
            }
        ]
    }
```


<!-- <img src="https://user-images.githubusercontent.com/33981376/99262849-1c62ba80-2827-11eb-99f2-ba52aa26236a.png" width="350" height="350"> -->

### Prediction Files Format

A prediction file, for example for the development set, must be one single JSON file for all tweets. The entry for each tweet must include the fields "id" and "labels". As an example, the input files described above would be also valid prediction files. In the case of task 2, each entry of the field labels must include the fields "start", "end", and "technique". We provide format checkers to automatically check the format of the submissions (see below). 

If you want to check the performance of your model on the development and test (when available) sets, upload your predictions' file to the website of the shared task: https://sites.google.com/view/propaganda-detection-in-arabic/. See instructions on the website about how to register and make a submission. 

## Format checkers

The format checkers for the subtask 1 are located in the [format_checker](format_checker) module of the project. The format checker verifies that your generated results file complies with the expected format. The format checker for subtask 2 is included in the scorer. 

Before running the format checker please install all prerequisites through,
> pip install -r requirements.txt

### Subtask 1:
To launch it, please run the following command:

```python
python3 format_checker/task1.py --pred_files_path=<path_to_your_results_files> --classes_file_path=<path_to_techniques_categories_for_task>
```
Example:
```
python3 format_checker/task1.py --pred_files_path=./baseline-output-task1-random.txt --classes_file_path=techniques_list_task1-2.txt
```
Note that the checker cannot verify whether the prediction file you submit contains all lines, because it does not have access to the corresponding gold file.

### Subtask 2:
Run the scorer to have the format of the input file checked. 

## Scorer and Official Evaluation Metrics

The scorer for the subtasks is located in the [scorer](scorer) module of the project. The scorer will report official evaluation metric and other metrics of a prediction file.

You can install all prerequisites through,
> pip install -r requirements.txt

### Subtask 1:

The **official evaluation metric** for the task is **micro-F1**. However, the scorer also reports macro-F1. 

To launch it, please run the following command:
```python
python3 scorer/task1.py --gold_file_path=<path_to_gold_labels> --pred_file_path=<path_to_your_results_file> --classes_file_path=<path_to_techniques_categories_for_task>
```
Example:
```
python3 task1.py --pred_file_path=./baseline-output-task1-random.txt --classes_file_path=../techniques_list_task1-2.txt --gold_file_path=./baseline-output-task1-random.txt
```
Note: You can set a flag ```-d```, to print out more detailed scores.


### Subtask 2:

Task 2 is a multi-label sequence tagging task. We modify the standard micro-averaged F1 to account for partial matching between the spans. More details of the evaluation measures can be found in the paper ["Fine-Grained Analysis of Propaganda in News Article"](https://aclanthology.org/D19-1565/)

In addition, an F1 value is computed for each propaganda technique.
```
cd scorer/; 
python3 task-2-semeval21_scorer.py -s prediction_file -r gold_labels_file -p ../techniques_list_task1-2.txt 
```

Example:
```
cd scorer/; 
python3 task-2-semeval21_scorer.py -s ../baseline-output-task1-random.txt -r ../data/task1_dev_test.json -p ../techniques_list_task1-2.txt
```

To access the command line help of the scorer type
```
python3 task-2-semeval21_scorer.py -h
```
Note that the option -d prints additional debugging information.



## Baselines

### Task 1

 * Random baseline
 ```
python3 baselines/baseline_task1_random.py
 ```
If you submit the predictions of the baseline on the development set to the shared task website, you would get a F1 score of 0.04494.

### Task 2

The baseline for task 2 simply creates random spans and technique names for the development set. No learning is performed. 
Run as
```
python3 baselines/baseline_task2.py
```
If you submit the predictions of the baseline on the development set to the shared task website, you would get a F1 score of 0.00699.
If you score the baseline on the training set (uncomment lines 5-6 in baseline_task2.py), you should get a F1 score of 0.038112
```
python3 scorer/task-2-semeval21_scorer.py -s prediction_file -r gold_labels_file -p techniques_list_task1-2.txt

```


## Licensing

These datasets are free for general research use.




## Citation


## Additional Resources
We listed the following tools/source code, which might be helpful to run the experiments.
* https://fasttext.cc/docs/en/supervised-tutorial.html
* https://huggingface.co/docs/transformers/training
* https://github.com/Tiiiger/bert_score
* https://github.com/clef2018-factchecking/clef2018-factchecking
* https://github.com/utahnlp/x-fact
* https://github.com/firojalam/COVID-19-disinformation/tree/master/bin


## Recommended reading
The following papers might be useful. We have not provided exhaustive list. But these could be a good start.<br>
[Download bibliography](bibtex/bibliography.bib)

**Propaganda**
* G. Da San Martino, S. Yu, A. Barrón-Cedeno, R. Petrov, and P. Nakov, **“Fine-grained analysis of propaganda in news article,”** in Proceedings of the 2019 conference on empirical methods in natural language processing and the 9th international joint conference on natural language processing (EMNLP-IJCNLP), 2019, p. 5636–5646.

* Dimitar Dimitrov, Bishr Bin Ali, Shaden Shaar, Firoj Alam, Fabrizio Silvestri, Hamed Firooz, Preslav Nakov and Giovanni Da San Martino, **Detecting Propaganda Techniques in Memes**, ACL, 2021. paper, Download dataset: https://github.com/di-dimitrov/propaganda-techniques-in-memes

* Dimitar Dimitrov, Bishr Bin Ali, Shaden Shaar, Firoj Alam, Fabrizio Silvestri, Hamed Firooz, Preslav Nakov and Giovanni Da San Martino, **SemEval-2021  Task 6: Detection of Persuasion Techniques in Texts and Images.**  SemEval, 2021. Task Data.

* P. Nakov and G. Da San Martino, “Fake News, Disinformation, Propaganda, Media Bias, and Flattening the Curve of the COVID-19 Infodemic,” in Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining, 2021, p. 4054–4055.

* P. Nakov and G. Da San Martino, **“Fake News, Disinformation, Propaganda, and Media Bias,”** in Proceedings of the 30th ACM International Conference on Information & Knowledge Management, 2021, p. 4862–4865.

* S. Yu, G. Da San Martino, M. Mohtarami, J. Glass, and P. Nakov, **“Interpretable Propaganda Detection in News Articles,”** in Proceedings of the International Conference on Recent Advances in Natural Language Processing (RANLP 2021), 2021, p. 1597–1605.

* Preslav Nakov, Firoj Alam, Shaden Shaar, Giovanni Da San Martino and Yifan Zhang, **COVID-19 in Bulgarian Social Media: Factuality, Harmfulness, Propaganda, and Framing**, RANLP, 2021.


**Fact-checking**
* Nakov, Preslav, David Corney, Maram Hasanain, Firoj Alam, and Tamer Elsayed. **["Automated Fact-Checking for Assisting Human Fact-Checkers."](https://www.ijcai.org/proceedings/2021/0619.pdf)** in IJCAI, 2021.

* Shaar, Shaden, Firoj Alam, Giovanni Da San Martino, and Preslav Nakov. **"Assisting the Human Fact-Checkers: Detecting All Previously Fact-Checked Claims in a Document."** arXiv preprint arXiv:2109.07410 (2021).

* Shaar, Shaden, Firoj Alam, Giovanni Da San Martino, and Preslav Nakov. **"The role of context in detecting previously fact-checked claims."** arXiv preprint arXiv:2104.07423 (2021).

**COVID-19 Infodemic**
* Alam, Firoj, Shaden Shaar, Fahim Dalvi, Hassan Sajjad, Alex Nikolov, Hamdy Mubarak, Giovanni Da San Martino et al. **["Fighting the COVID-19 Infodemic: Modeling the Perspective of Journalists, Fact-Checkers, Social Media Platforms, Policy Makers, and the Society."](https://aclanthology.org/2021.findings-emnlp.56.pdf)** In Findings of the Association for Computational Linguistics: EMNLP 2021, pp. 611-649. 2021.

* Shaar, Shaden, Firoj Alam, Giovanni Da San Martino, Alex Nikolov, Wajdi Zaghouani, Preslav Nakov, and Anna Feldman. **"Findings of the NLP4IF-2021 Shared Tasks on Fighting the COVID-19 Infodemic and Censorship Detection."** In Proceedings of the Fourth Workshop on NLP for Internet Freedom: Censorship, Disinformation, and Propaganda, pp. 82-92. 2021.

* Nakov, Preslav, Firoj Alam, Shaden Shaar, Giovanni Da San Martino, and Yifan Zhang. **"A Second Pandemic? Analysis of Fake News about COVID-19 Vaccines in Qatar."** In Proceedings of the International Conference on Recent Advances in Natural Language Processing (RANLP 2021), pp. 1010-1021. 2021.
* Nakov, Preslav, Firoj Alam, Shaden Shaar, Giovanni Da San Martino, and Yifan Zhang. **"COVID-19 in Bulgarian social media: Factuality, harmfulness, propaganda, and framing."** In Proceedings of the International Conference on Recent Advances in Natural Language Processing (RANLP 2021), pp. 997-1009. 2021.

**CLEF Shared Tasks papers**
* Preslav Nakov, Alberto Barrón-Cedeño, Giovanni Da San Martino, Firoj Alam, Ruben Miguez, Tommaso Caselli, Mucahid Kutlu, Wajdi Zaghouani, Chengkai Li, Shaden Shaar, Hamdy Mubarak, Alex Nikolov, Yavuz Selim Kartal, **Overview of the CLEF-2022 CheckThat! lab Task 1 on Identifying Relevant Claims in Tweets**, in: Working Notes of CLEF 2022—Conference and Labs of the Evaluation Forum, CLEF ’2022, Bologna, Italy, 2022.

* Preslav Nakov, Giovanni Da San Martino, Firoj Alam, Shaden Shaar, Hamdy Mubarak, Nikolay Babulkov, **Overview of the CLEF-2022 CheckThat! Lab Task 2 on Detecting Previously Fact-Checked Claims**, in: Proceedings of the 13th International Conference of the CLEF Association: Information Access Evaluation meets Multilinguality, Multimodality, and Visualization, CLEF ’2022, Bologna, Italy, 2022.

* P.Nakov, A.Barrón-Cedeño, G.Da San Martino, F.Alam, J.M.Struß, T.Mandl, R.Míguez, T. Caselli, M. Kutlu, W. Zaghouani, C. Li, S. Shaar, G. K. Shahi, H. Mubarak, A. Nikolov, N. Babulkov, Y. S. Kartal, J. Beltrán, M. Wiegand, M. Siegel, J. Köhler, **Overview of the CLEF-2022 CheckThat! lab on Fighting the COVID-19 Infodemic and Fake News Detection**, in: Proceedings of the 13th International Conference of the CLEF Association: Information Access Evaluation meets Multilinguality, Multimodality, and Visualization, CLEF ’2022, Bologna, Italy, 2022.

* Nakov, Preslav, Giovanni Da San Martino, Tamer Elsayed, Alberto Barrón-Cedeño, Rubén Míguez, Shaden Shaar, Firoj Alam et al. **"Overview of the CLEF–2021 CheckThat! Lab on Detecting Check-Worthy Claims, Previously Fact-Checked Claims, and Fake News."** In International Conference of the Cross-Language Evaluation Forum for European Languages, pp. 264-291. Springer, Cham, 2021.
* Shaar, Shaden, Maram Hasanain, Bayan Hamdan, Zien Sheikh Ali, Fatima Haouari, Alex Nikolov, Mücahid Kutlu et al. **"Overview of the CLEF-2021 CheckThat! lab task 1 on check-worthiness estimation in tweets and political debates."** In CLEF (Working Notes). 2021.
* Shahi, Gautam Kishore, Julia Maria Struß, and Thomas Mandl. **"Overview of the CLEF-2021 CheckThat! lab task 3 on fake news detection."** Working Notes of CLEF (2021).
* Shaar, Shaden, Fatima Haouari, Watheq Mansour, Maram Hasanain, Nikolay Babulkov, Firoj Alam, Giovanni Da San Martino, Tamer Elsayed, and Preslav Nakov. **"Overview of the CLEF-2021 CheckThat! lab task 2 on detecting previously fact-checked claims in tweets and political debates."** In CLEF (Working Notes). 2021.
* Barrón-Cedeño, Alberto, Tamer Elsayed, Preslav Nakov, Giovanni Da San Martino, Maram Hasanain, Reem Suwaileh, Fatima Haouari et al. **"Overview of CheckThat! 2020: Automatic identification and verification of claims in social media."** In International Conference of the Cross-Language Evaluation Forum for European Languages, pp. 215-236. Springer, Cham, 2020.
* Shaar, Shaden, Alex Nikolov, Nikolay Babulkov, Firoj Alam, Alberto Barrón-Cedeno, Tamer Elsayed, Maram Hasanain et al. **"Overview of CheckThat! 2020 English: Automatic identification and verification of claims in social media."** In International Conference of the Cross-Language Evaluation Forum for European Languages. 2020.
* Hasanain, Maram, Fatima Haouari, Reem Suwaileh, Zien Sheikh Ali, Bayan Hamdan, Tamer Elsayed, Alberto Barrón-Cedeno, Giovanni Da San Martino, and Preslav Nakov. **"Overview of CheckThat! 2020 Arabic: Automatic identification and verification of claims in social media."** In International Conference of the Cross-Language Evaluation Forum for European Languages. 2020.
* Elsayed, Tamer, Preslav Nakov, Alberto Barrón-Cedeno, Maram Hasanain, Reem Suwaileh, Giovanni Da San Martino, and Pepa Atanasova. **"Overview of the CLEF-2019 CheckThat! Lab: automatic identification and verification of claims."** In International Conference of the Cross-Language Evaluation Forum for European Languages, pp. 301-321. Springer, Cham, 2019.
* Elsayed, Tamer, Preslav Nakov, Alberto Barrón-Cedeno, Maram Hasanain, Reem Suwaileh, Giovanni Da San Martino, and Pepa Atanasova. **"CheckThat! at CLEF 2019: Automatic identification and verification of claims."** In European Conference on Information Retrieval, pp. 309-315. Springer, Cham, 2019.
* Atanasova, Pepa, Preslav Nakov, Georgi Karadzhov, Mitra Mohtarami, and Giovanni Da San Martino. **"Overview of the CLEF-2019 CheckThat! Lab: Automatic Identification and Verification of Claims. Task 1: Check-Worthiness."** CLEF (Working Notes) 2380 (2019).
* Nakov, Preslav, Alberto Barrón-Cedeno, Tamer Elsayed, Reem Suwaileh, Lluís Màrquez, Wajdi Zaghouani, Pepa Atanasova, Spas Kyuchukov, and Giovanni Da San Martino. **"Overview of the CLEF-2018 CheckThat! Lab on automatic identification and verification of political claims."** In International conference of the cross-language evaluation forum for european languages, pp. 372-387. Springer, Cham, 2018.
* Barrón-Cedeno, Alberto, Tamer Elsayed, Reem Suwaileh, Lluís Màrquez, Pepa Atanasova, Wajdi Zaghouani, Spas Kyuchukov, Giovanni Da San Martino, and Preslav Nakov. **"Overview of the CLEF-2018 CheckThat! Lab on Automatic Identification and Verification of Political Claims. Task 2: Factuality."**   CLEF (Working Notes) 2125 (2018).
* Atanasova, Pepa, Alberto Barron-Cedeno, Tamer Elsayed, Reem Suwaileh, Wajdi Zaghouani, Spas Kyuchukov, Giovanni Da San Martino, and Preslav Nakov. **"Overview of the CLEF-2018 CheckThat! lab on automatic identification and verification of political claims. Task 1: Check-worthiness."** arXiv preprint arXiv:1808.05542 (2018).


