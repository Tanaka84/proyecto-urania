import os
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from dicval.models import Diccionario
from nltk.stem import SnowballStemmer
import stanza
import emoji


def fetch_key(file):

    file_path = os.path.join(r'/home/ubuntu/django/urania', r'analyzer/keys', file)
    with open(file_path, 'r') as key:
        string = key.read()
        return string


def clean_text(text, query, language):
    # limpia el texto
    text_to_analyze = text
    text_to_analyze = text_to_analyze.lower()
    # Remueve @
    text_to_analyze = re.sub("@\S+", " ", text_to_analyze)
    # Remueve https
    text_to_analyze = re.sub("https*\S+", " ",  text_to_analyze)
    # Remueve hashtag
    text_to_analyze = re.sub("#\S+", " ", text_to_analyze)
    text_to_analyze = re.sub(r'\'\w+', '', text_to_analyze)
    text_to_analyze = re.sub(r'\w*\d+\w*', '', text_to_analyze)
    text_to_analyze = re.sub('\s{2,}', " ",  text_to_analyze)
    text_to_analyze = re.sub('/(\brt\b)/g', " ",  text_to_analyze)
    text_to_analyze = re.sub('¿', " ",  text_to_analyze)
    text_to_analyze = re.sub('──', " ",  text_to_analyze)

    text_to_analyze = text_to_analyze.replace('\u2026', "")
    text_to_analyze = text_to_analyze.translate(
        str.maketrans('', '', string.punctuation))
    text_to_analyze = deEmojify(text_to_analyze)

    # Tokenizar y pasar a lista para quitar las stopwords
    tokenizacion = word_tokenize(text_to_analyze)
    if language == 'es':
        stop_words = set(stopwords.words("spanish"))
    elif language == 'en':
        stop_words = set(stopwords.words("english"))
    texto_tokenizado_limpio = []
    query_2 = query.lower()
    query_list = query_2.split(' ')

    for word in tokenizacion:
        try:
            Diccionario.objects.get(palabra=word)
            if word not in stop_words and word not in query_list and len(word) > 3:
                texto_tokenizado_limpio.append(word)
        except:
            continue
    
    spanish_stemmer = SnowballStemmer('spanish')
    
    #for i in range(0,len(texto_tokenizado_limpio)):
    #    texto_tokenizado_limpio[i] = spanish_stemmer.stem(texto_tokenizado_limpio[i])
    #    print(texto_tokenizado_limpio[i]) 
    return texto_tokenizado_limpio


#def lematizar(lista, language):
#
#    texto_a_lematizar = " ".join(lista)
#    nlp_lenma = stanza.Pipeline(
#        lang=language, processors='tokenize,mwt,pos,lemma')
#    resultado = nlp_lenma(texto_a_lematizar)
#    lista_de_tokens = [
#        word.lemma for sent in resultado.sentences for word in sent.words]
#    return lista_de_tokens


def deEmojify(text):
    demojifiedtext = re.sub(emoji.get_emoji_regexp(), r"", text)
    return demojifiedtext
