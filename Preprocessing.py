from html.parser import HTMLParser
import pickle
import re
import string
from nltk.stem import PorterStemmer
import os
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.corpus import stopwords
filenames,tf,docnum_tokens=[],{},{}
for filename in os.listdir("C:\\Users\\srika\\OneDrive\\Desktop\\Spring20\\Subjects\\IR\\Assignments\\final_project\\Crawled_data"):
    filenames.append(filename)
def preprocess_text(body):
    soup,val=BeautifulSoup(body,'html.parser'),[]
    all_texts = soup.findAll(text=True)
    for check in all_texts:
        if check.parent.name not in ['style', 'script', 'head', 'meta', '[document]'] and isinstance(check,Comment)==False:
            val.append(check)
    text= u" ".join(t.strip() for t in val)
    all_words = " ".join(re.findall("[a-zA-Z0-9]+", text))
    text = ''.join(word.lower() for word in all_words if not word.isdigit())
    words = text.split(" ")
    return words 
    
def extract():
    ps,stop_words = PorterStemmer(),set(stopwords.words('english'))
    for filename in filenames:
        html_format = open("C:\\Users\\srika\\OneDrive\\Desktop\\Spring20\\Subjects\\IR\\Assignments\\final_project\\Crawled_data"+"\\"+filename,"r",encoding="utf-8") 
        html=html_format.read()
        final_text=preprocess_text(html)
        f= [ps.stem(x) for x in final_text if ps.stem(x) not in stop_words and len(ps.stem(x))>2]              #Removes stop words and performs stemming
        for token in f:
            tf.setdefault(token,{})[filename]= tf.setdefault(token, {}).get(filename, 0) + 1
            
        docnum_tokens[filename]=f

def calc_term_freq():
    with open('tf.pickle', 'wb') as f:
        pickle.dump(tf, f)

def store_docnum_tokens():
    with open('docnum_tokens.pickle', 'wb') as f:
        pickle.dump(docnum_tokens, f)

            
extract()
calc_term_freq()
store_docnum_tokens()