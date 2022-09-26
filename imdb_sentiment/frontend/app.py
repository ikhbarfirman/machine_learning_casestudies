import json
import numpy as np
import streamlit as st
import requests
import pickle
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
import string
import requests

# load pipeline
proc = pickle.load(open("model/preprocess_text.pkl", "rb"))
stop_words = list(STOPWORDS)
stemmer = PorterStemmer()
lemma = WordNetLemmatizer()

def full_remove(x, removal_list): 
    for w in removal_list:
        x = x.replace(w, ' ')
    return x

stop_words.extend(['s','ve','t','nt','m','ll']) #Menambahkan stop words list

def text_processing_2(text):
  text = text.lower() #Set lowercase pada kata
  text = re.sub(r"http\S+", " ", text) #Menghilangkan link
  text = re.sub(r"www.\S+", " ", text) #Menghilangkan link
  text = re.sub(r"\n"," ",text) #Menghilangkan \n
  text = ' '.join([full_remove(x, list(string.punctuation)) for x in text.split()]) #Menghilangkan punctuation
  text = text.strip() #Menghilangkan spasi kosong ataupun tab pada awal dan akhir kalimat
  text = re.sub("[^A-Za-z\s']"," ", text) #Menghilangkan yang bukan huruf
  tokens = word_tokenize(text) # Mendeteksi token pada kalimat
  text = [lemma.lemmatize(word) for word in tokens if word not in stop_words]
  text = ' '.join(text)
  return text    

st.title("Sentiment Prediction")


review = st.text_input("Masukkan review movie")
review_proc = text_processing_2(review)
X_inf = np.array([review_proc])
X_inf_ready = proc.transform(X_inf).toarray()


# inference
URL = "http://backend-ikhbar-fin.herokuapp.com/v1/models/review_model:predict"
param = json.dumps({
        "signature_name":"serving_default",
        "instances":X_inf_ready.tolist()
    })
r = requests.post(URL, data=param)
if r.status_code == 200:
    res = r.json()
    ind = np.argmax(res['predictions'][0])
    if ind == 0: st.title("Sentiment review: Negative")
    elif ind == 1: st.title("Sentiment review: Neutral")
    else: st.title("Sentiment review: Positive")
else:
    st.title("Unexpected Error")    
 