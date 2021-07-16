from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Diccionario, Votos
import random


# Create your views here.


def entrada(request):
    return HttpResponse("Aqui va el validador de diccionario")


@login_required
def presentacion(request):
    # recupera el usuario del request para el saludo
    user = request.user
    # recupera la cantidad de veces que el usuario ha votado
    no_de_votos = Votos.objects.filter(usuario=request.user).count()
    # construye el contexto para pasarlo al templete
    context = {"user": user, "no_de_votos": no_de_votos}
    return render(request, template_name="presentacion.html", context=context)


@login_required
def cierre(request):
    # recupera el usuario del request para el saludo
    user = request.user
    # recupera la cantidad de veces que el usuario ha votado
    no_de_votos = Votos.objects.filter(usuario=request.user).count()
    # construye el contexto para pasarlo al templete
    context = {"user": user, "no_de_votos": no_de_votos}
    return render(request, template_name="despedida.html", context=context)


@login_required
def pagina_de_votos(request):
    if request.method == "GET":
        if request.is_ajax():
            palabra = Diccionario.objects.all().order_by('no_de_votos')[0]
            palabra.no_de_votos = palabra.no_de_votos + 1
            palabra.save()
            return JsonResponse({"id": palabra.id, "palabra": palabra.palabra})
        else:
            palabra = Diccionario.objects.all().order_by('no_de_votos')[0]
            palabra.no_de_votos = palabra.no_de_votos + 1
            palabra.save()
            context = {"pal": palabra}
            return render(request, template_name="votos.html", context=context)
    if request.method == "POST":

        voto = Votos(usuario=request.user,
                     palabra=Diccionario.objects.get(id=request.POST['palabra']), voto=request.POST['vote'])
        voto.save()

        if Diccionario.objects.get(id=request.POST['palabra']).no_de_votos > 100:
            total_score = Votos.objects.filter(palabra=Diccionario.objects.get(
                id=request.POST['palabra'])).aggregate(Sum('voto'))
            new_sentiment = Diccionario.objects.get(id=request.POST['palabra'])
            if total_score > 10:
                new_sentiment.sentimiento = 1
                new_sentiment.save()
            elif total_score < -10:
                new_sentiment.sentimiento = -1
                new_sentiment.save()
            else:
                new_sentiment.sentimiento = 0
                new_sentiment.save()
        return HttpResponse("")
