import pandas as pd
import spacy
import collections

cols = ['text','author','title']
df = pd.read_table("/Users/nosuke/Desktop/2022_1st_half/Datamining/report3/out_files/level1.txt",sep=",", header=0, names=['num', 'text', 'author', 'title'])
df = df.drop('num',axis=1)

nlp = spacy.load("ja_ginza")

def count_lemma3(df, column, target_poses, stop_words):
    '''分かち書き3:原形処理し、ストップワードを除き、品詞別にカウント。
    args:
      df (pd.DataFrame): 読み込み対象データフレーム。
      column (str): データフレーム内の読み込み対象列名。
      target_poses ([str]): カウント対象となる品詞名のリスト。
      stop_words ([str]): 削除したい単語のリスト。
    return
      words_dict ({pos1:{token1.lemma_:i, token2.lemma_:j},
                   pos2:{token3.lemma_:k, token4.lemma_:l}}): 品詞(pos)別に、単語をカウント。
    '''
    words_dict = {}
    for pos in target_poses:
        words_dict[pos] = {}

    for comment in df[column]:
        doc = nlp(comment)
        for token in doc:
            if token.lemma_ not in stop_words:
                if token.pos_ in target_poses:
                    if token.lemma_ not in words_dict[token.pos_]:
                        words_dict[token.pos_].update({token.lemma_: 1})
                    else:
                        words_dict[token.pos_][token.lemma_] += 1
    return words_dict

target_poses = ['PROPN', 'NOUN', 'VERB', 'ADJ', 'ADV']
stop_words = ['だ','よう','こと','ある','いる','ない','いう','する','なる']
words_dict = count_lemma3(df, 'text', target_poses, stop_words)

for pos in target_poses:
    print('pos = ', pos)
    words_dict[pos] = collections.Counter(words_dict[pos])
    print(words_dict[pos].most_common(10))

print("総単語数")
all_words = {**words_dict['PROPN'], **words_dict['NOUN'], **words_dict['VERB'], **words_dict['ADJ'], **words_dict['ADV']}
print(len(all_words))

for comment in df['text']:
    doc = nlp(comment)
    for entity in doc.ents:
        print(entity.text, entity.label_)

print(df[df['text'].str.contains('神経')])
print(df[df['text'].str.contains('絵具')])