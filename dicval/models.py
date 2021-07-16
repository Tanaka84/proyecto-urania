from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Crea la tabla para las palabras

class Diccionario(models.Model):
    # Columna de la palabra, se graba como string
    palabra = models.CharField(max_length=250)
# Columna para grabar el sentimiento de cada palabra, donde -1 es negativo, 1 es positivo y 0 es neutro
    sentimiento = models.IntegerField()
    no_de_votos = models.IntegerField(default=0)

# Definir lo que se recupera cuando pedimos el nombre del objecto
    def __str__(self):
        return self.palabra
    # Crea la tabla para registar los votos


class Votos(models.Model):
    # Columna: PK del usuario que votó
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
# Columna: PK de la palabra vatada
    palabra = models.ForeignKey(Diccionario, on_delete=models.CASCADE)
# Columna: PK del voto en numero
    voto = models.IntegerField()
# Definir lo que se recupera cuando pedimos el nombre del objecto

    def __str__(self):
        return str(self.palabra)
