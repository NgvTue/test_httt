import os,json,sys
import numpy as np 
import pandas as pd
from sklearn.naive_bayes import CategoricalNB,MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import re
import pickle
from src.pipeline import PipeLine
def clean_text(sent):

    re_punc = re.compile("([\"\''().,;:/_?!—\-])")

    sent = re_punc.sub(r" ", sent)
    
    return sent 



with open("/home/tuenguyen/speech/httt/datasets/training_set.json","r") as f:
    training_set = json.load(f)

    train = []
    for key in training_set:
        for sample in training_set[key]:
            train.append(
                {
                    'label':key,
                    'sentence':sample[0]['value']
                }
            )
    train.append({"label":"tra cứu luật","sentence":"cho mình hỏi thông tin luật"})
    train.append({"label":"tra cứu luật","sentence":"cho mình hỏi luật này với"})
    train.append({"label":"tra cứu luật","sentence":"cho mình hỏi luật này với bạn"})
    # train.append({"label":"tra cứu luật","sentence":"cho mình hỏi thông tin luật với bạn"})
    # train.append({"label":"tra cứu luật","sentence":"luật này được quy định như thế nào"})
    # train.append({"label":"tra cứu luật","sentence":"luật này được quy định ra sao"})
    # train.append({"label":"tra cứu luật","sentence":"quy định của luật này"})
    # train.append({"label":"tra cứu luật","sentence":"cho mình thêm thông tin luật"})
    # train.append({"label":"tra cứu luật","sentence":"cho mình biết thông tin luật"})
    # train.append({"label":"tra cứu luật","sentence":"cho mình hiểu thông tin luật"})
    # train.append({"label":"tra cứu cầu thủ","sentence":"cho mình hỏi thông tin cầu thủ"})
    train = pd.DataFrame(train)
    train.label = train.label.map({
        'tra cứu luật':0,
        'tình huống':1,
        'tra cứu cầu thủ':2,
        'tra cứu bảng xếp':3,
        'kết thúc trò chuyện':4
    })
    train = train.sample(frac=1).reset_index(drop=True)

    print(train.head(2))
with open("/home/tuenguyen/speech/httt/datasets/testing_set.json","r") as f:
    testing_set = json.load(f)

    test = []
    for key in testing_set:
        for sample in testing_set[key]:
            test.append(
                {
                    'label':key,
                    'sentence':sample[0]['value']
                }
            )
    test = pd.DataFrame(test)
    test.label = test.label.map({
        'tra cứu luật':0,
        'tình huống':1,
        'tra cứu cầu thủ':2,
        'tra cứu bảng xếp':3,
        'kết thúc trò chuyện':4
    })
    test = test.sample(frac=1).reset_index(drop=True)

    print(test.head(2))



corpus = train.sentence.apply(clean_text).values
vectorizer = CountVectorizer(ngram_range=(1,3))
X_train = vectorizer.fit_transform(np.asarray(corpus)).todense()
X_test  =vectorizer.transform( np.asarray(test.sentence.apply(clean_text).values)).todense()
X_test = np.asarray(X_test)

clf = MultinomialNB()
clf.fit(X_train, train.label.values)
pred = clf.predict(X_test)
sc= clf.score(X_test, test.label.values)

print(f"Scoring in testset  = {sc}")

pipeline = PipeLine()
pipeline.add_pipe(vectorizer)
pipeline.add_pipe(clf)
pipeline.save("./model_pipeline.pkl")

pipeline = PipeLine.load("./model_pipeline.pkl")
vectorizer = pipeline.pipe[0]
clf =pipeline.pipe[1]
def hard_code(prob,corpus_t):
    key_word_rule = ['luật',"quy định","nội quy"]
    key_word_per = ['person',"cầu thủ","người","cậu thủ"]
    key_word_ac  =['tình huống', "trường hợp"]
    for t in key_word_rule:
        if t in corpus_t:
            prob[:,0] += 0.3
    for t in key_word_per:
        if t in key_word_rule:
            prob[:,2] += 0.3
    for t in key_word_ac:
        if t in corpus_t:
            prob[:,1] += 0.3
    prob = np.where(prob < 0.99, prob, 0.99)
    return prob
def predict(corpus_t):
    if isinstance(corpus_t, str):
        corpus_test = [corpus_t]
    else:
        corpus_test=[i for i in corpus_t]
    
    clean_corpus = np.asarray([clean_text(i) for i in corpus_test])
    print(clean_corpus)

    vector_corpus = np.asarray(vectorizer.transform(clean_corpus).todense())
    
    # vector_corpus = np.where(vector_corpus>1,1,vector_corpus)
    
    predict_corpus = clf.predict(vector_corpus)
    prob = clf.predict_proba(vector_corpus)
    prob = hard_code(prob,corpus_t)
    prob = np.max(prob,-1) # lay max cac nhan
    predict_corpus = [
        {
        0: 'tra cứu luật',
        1: 'tình huống',
        2: 'tra cứu cầu thủ',
        3: 'tra cứu bảng xếp hạng',
        4: 'kết thúc trò chuyện'
        }[i] for i in predict_corpus

    ]
    predict_corpus= [{
        'p':i,
        'value':j,
        'text': t} for (i,j,t) in zip(prob, predict_corpus, corpus_test)
    ]
    return predict_corpus

# corpus_test= [
#     'cho em thông tin bảng xếp hạng được hông?'
# ]
# clean_corpus =np.asarray([clean_text(i) for i in corpus_test])
# vector_corpus = vectorizer.transform(clean_corpus).todense()
# predict_corpus = clf.predict(vector_corpus)
# predict_corpus = [
#     {
#        0: 'tra cứu luật',
#        1: 'tình huống',
#        2: 'tra cứu cầu thủ',
#        3: 'tra cứu bảng xếp hạng',
#        4: 'kết thúc trò chuyện'
#     }[i] for i in predict_corpus

# ]
# print(predict_corpus)



# pipeline = PipeLine()

# pipeline.add_pipe(
#     vectorizer
# )

# pipeline.add_pipe(
#     clf
# )

# pipeline.save("./model_pipeline.pkl")
# del pipeline 
# pipeline = PipeLine.load("./model_pipeline.pkl")
# vectorizer = pipeline.pipe[0]
# clf =pipeline.pipe[1]

# corpus_test= [
#     'cho em thông tin bảng xếp hạng được hông?'
# ]
# clean_corpus = np.asarray([clean_text(i) for i in corpus_test])
# vector_corpus = np.asarray(vectorizer.transform(clean_corpus).todense())
# predict_corpus = clf.predict(vector_corpus)
# predict_corpus = [
#     {
#        0: 'tra cứu luật',
#        1: 'tình huống',
#        2: 'tra cứu cầu thủ',
#        3: 'tra cứu bảng xếp hạng',
#        4: 'kết thúc trò chuyện'
#     }[i] for i in predict_corpus

# ]
# print(predict_corpus)