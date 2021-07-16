import pandas as pd
from dicval.models import Diccionario

data_de_palabras = pd.read_csv('/home/ubuntu/django/urania/Diccionario.csv')


for index, row in data_de_palabras.iterrows():
    try:
        Diccionario.objects.get(palabra=row['Spanish (es)'])
        continue
    except:
        if row['Spanish (es)'] == "NO TRANSLATION":
            continue
        if len(row['Spanish (es)']) > 30:
            continue
        if row['Positive'] == 1 and row['Negative'] == 0:
            p = Diccionario(palabra=row['Spanish (es)'], sentimiento=1)
            p.save()
        elif row['Positive'] == 0 and row['Negative'] == 1:
            p = Diccionario(palabra=row['Spanish (es)'], sentimiento=-1)
            p.save()
        else:
            p = Diccionario(palabra=row['Spanish (es)'], sentimiento=0)
            p.save()
