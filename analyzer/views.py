from pickle import TRUE
from django.db.models import query
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import tweepy as tw
from collections import Counter
from nltk import FreqDist
from dicval.models import Diccionario
from .scripts import fetch_key, clean_text

# Create your views here.

CONSUMER_KEY = fetch_key("API.txt")
CONSUMER_SECRET = fetch_key("APIsecret.txt")
ACCESS_TOKEN = fetch_key("access.txt")
ACCESS_TOKEN_SECRET = fetch_key("access_secret.txt")


@login_required
def twitter_fetch(request):
    if request.method == "GET":
        return render(request, template_name='twitter.html')
    if request.method == 'POST':
        query = request.POST['query']
        no_of_tweets = int(request.POST['number_of_tweets'])
        language = 'es'
        auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tw.API(auth)
        text_to_analyze = []
        last_id = -1
        while len(text_to_analyze) < no_of_tweets:
            count = no_of_tweets - len(text_to_analyze)
            try:
                new_tweets = api.search(
                    q=query, count=count, max_id=str(last_id - 1), lang=language)
                if not new_tweets:
                    break
                for tweet in new_tweets:
                    text_to_analyze.append(tweet.text)
                last_id = new_tweets[-1].id
            except tw.TweepError as e:
                break
        text_to_analyze = " ".join(text_to_analyze)
        lista_de_tokens = clean_text(text_to_analyze, query, language)
        if len(lista_de_tokens) < 100:
            return render(request, template_name = 'twitter.html', context = {"disculpa":"Perdon, no hemos encontrado suficientes palabras para correr el análisis, intenta despues, aumenta la cantidad de tuits o cambia la palabra clave"})
        request.session['lista_de_tokens'] = lista_de_tokens
        request.session['query'] = query
        return redirect('analyze')


@login_required
def analyze(request):
    lista_de_tokens = request.session.get('lista_de_tokens')
    query = request.session.get('query')
    positive_counter = 0
    negative_counter = 0
    total_counter = 0
    for token in lista_de_tokens:
        try:
            if Diccionario.objects.get(palabra=token).sentimiento == 1:
                positive_counter += 1
                total_counter += 1
            elif Diccionario.objects.get(palabra=token).sentimiento == -1:
                negative_counter += 1
                total_counter += 1
            elif Diccionario.objects.get(palabra=token).sentimiento == 0:

                total_counter += 1
        except:
            continue
    try:
        analisis_de_sentimiento = round((positive_counter - negative_counter)/total_counter, 3)
        negatividad = round(negative_counter/total_counter, 3)
        ratio = round(((positive_counter+negative_counter)/total_counter)*100, 2)
        if analisis_de_sentimiento < 0:
            polaridad = 'negativa'
        if analisis_de_sentimiento > 0:
            polaridad = 'positiva'
        frecuencia = Counter(lista_de_tokens).most_common(
            int(round(len(lista_de_tokens)/2, 0)))
        lista_de_palabras_comunes = [word for word, count in frecuencia]
        lista_de_frecuencias = [count for word, count in frecuencia]
        ctx = {'positive_counter': positive_counter, 'negative_counter': negative_counter, 'query': query, 'negatividad': negatividad, 'analisis': analisis_de_sentimiento,
           'ratio': ratio, 'polaridad': polaridad, "lista_de_palabras_comunes": lista_de_palabras_comunes, 'lista_de_frecuencias': lista_de_frecuencias}
        return render(request, template_name='analyze.html', context=ctx)
    except:
        return render(request, template_name='twitter.html', context= {"disculpa": "Perdon, parece que algo ha salido mal, espera un poco o intenta cambiar algunos criterios de tu busqueda"} )
