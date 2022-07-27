import pandas as pd
import re
import glob

def conv(dl_text):
    with open(dl_text, 'r', encoding="shift-jis") as d:
        text = d.read() 
    fited_text = text.split()
    title  = fited_text[0]
    auther = fited_text[1]
    text = re.split(r'\-{5,}', text)[2] 
    text = re.split(r'底本：', text)[0] 
    text = re.split(r'［＃改ページ］', text)[0] 
    text = re.sub(r'「', '', text) 
    text = re.sub(r'」', '', text) 
    text = re.sub(r'《.+?》', '', text) 
    text = re.sub(r'［＃.+?］', '', text) 
    text = re.sub(r'｜', '', text)  
    text = re.sub(r'\r\n', '', text)  
    text = re.sub(r'\n', '', text) 
    text = re.sub(r'\u3000', '', text)
    text = re.sub(r'、', '', text)
    text = re.sub(r'―', '', text)
    text = re.sub(r'', '', text)  
    text = text.split("。")
    text = list(filter(lambda a: a != "", text))
    return auther,title,text

txt_file = glob.glob("/Users/nosuke/Desktop/2022_1st_half/Datamining/report3/data/wagahaiwa_nekodearu.txt")

cols = ['text','author','title']
df = pd.DataFrame(columns=cols)

for file in txt_file:
    auther,title,text = conv(file)
    for i in range(len(text)):
        add_data = pd.Series({'text':text[i],'author':auther,'title':title})
        df = df.append(add_data, ignore_index=True)

print(df.head(10))
#print(df.tail(4))
df.to_csv("/Users/nosuke/Desktop/2022_1st_half/Datamining/report3/out_files/level1.txt")