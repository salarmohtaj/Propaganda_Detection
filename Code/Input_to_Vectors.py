import torch
from transformers import BertTokenizer, BertConfig, BertModel
import re
from torchtext.legacy.data import Field, TabularDataset, BucketIterator
import pickle
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')



bertmodel = 'asafaya/bert-base-arabic'
MAX_LEN = 32
tokenizer = BertTokenizer.from_pretrained(bertmodel)


def text_preprocess(text):
    text = re.sub("@([A-Za-z0-9_]+)", "username", text)
    text = re.sub(r"http\S+", "weblink", text)
    # text = demoji.replace_with_desc(text, sep=" ")
    text = re.sub("[ ]+", " ", text)
    return text


def bert_tokenize(text):
    text = text_preprocess(text)
    return tokenizer.tokenize(text)[:MAX_LEN - 2]


def my_tokenizer(text):
    text = text_preprocess(text)
    return text.split(" ")[:MAX_LEN - 2]


def tokenize_and_cut(text):
    text = text_preprocess(text)
    tokens = tokenizer.tokenize(text)
    tokens = tokens[:MAX_LEN-2]
    return tokens


text_field = Field(batch_first = True,
                  use_vocab = False,
                  tokenize = tokenize_and_cut,
                  preprocessing = tokenizer.convert_tokens_to_ids,
                  init_token = tokenizer.cls_token_id,
                  eos_token = tokenizer.sep_token_id,
                  pad_token = tokenizer.pad_token_id,
                  unk_token = tokenizer.unk_token_id)
id_field = Field(sequential=False, use_vocab=False)
fields = [("id", id_field), ('text', text_field), (None, None)]
train, dev, test = TabularDataset.splits(path="../data",
                                         train="task1_train.tsv", validation="task1_dev.tsv",
                                         test="task1_dev_test.tsv",
                                         format='tsv', skip_header=True, fields=fields)

train_iter = BucketIterator(train, batch_size=1, sort_key=lambda x: len(x.text),
                            device=DEVICE, sort=True, sort_within_batch=True)
dev_iter = BucketIterator(dev, batch_size=1, sort_key=lambda x: len(x.text),
                          device=DEVICE, sort=True, sort_within_batch=True)
dev_test_iter = BucketIterator(test, batch_size=1, sort_key=lambda x: len(x.text),
                               device=DEVICE, sort=True, sort_within_batch=True)


config = BertConfig.from_pretrained(bertmodel, output_hidden_states=True)
bert = BertModel.from_pretrained(bertmodel, config=config)
dic_train = {}

def inp_to_vec(iter):
    dic = {}
    for item in iter:
        with torch.no_grad():
            # embedded = self.bert(text)[0]
            embedded = bert(item.text)[0]
            # embedded = bert(item.text)
            # cat_vec = torch.stack(embedded[2])
            # embedded = torch.mean(cat_vec[-6:], dim=0)
            # print(embedded.size())
            embedded = torch.mean(embedded, 1).squeeze(0)
            # print(embedded.cpu().detach().numpy().size)
            # print(item.id.item())
            dic[item.id.item()] = embedded.cpu().detach().numpy()
    return dic

dic = inp_to_vec(train_iter)
dic_train.update(dic)
dic = inp_to_vec(dev_iter)
dic_train.update(dic)
dic = inp_to_vec(dev_test_iter)
dic_train.update(dic)


fields = [("id", id_field), ('text', text_field)]
test = TabularDataset(path="../data/task1_test.tsv", format='tsv', skip_header=True, fields=fields)


test_iter = BucketIterator(test, batch_size=1, sort_key=lambda x: len(x.text),device=DEVICE, sort=True, sort_within_batch=True)

dic_test = inp_to_vec(test_iter)
print(len(dic_train), len(dic_test))

with open("vec/train_dic.DIC","wb") as f:
    pickle.dump(dic_train, f)
with open("vec/test_dic.DIC","wb") as f:
    pickle.dump(dic_test, f)
