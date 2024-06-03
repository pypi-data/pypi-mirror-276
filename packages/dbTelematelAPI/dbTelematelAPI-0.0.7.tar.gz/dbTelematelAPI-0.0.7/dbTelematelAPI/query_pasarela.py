# -*- coding: utf-8 -*-

import requests
from time import time

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def convert_to_obj(rows):
    obj = []
    for row in rows:
        obj.append((Struct(**row)))
    return obj

def get_query_pasarela(url, db_name, query, token, timeout=0.0):
    """Hace un requests.GET y devuelve el resultado en un JSON

    Args:
        url (string): Url dónde se hace el GET
        db_name (string): Nombre de la base de datos ('mypartes', 'tlmplus', 'tlmplus1' o 'tlmplus2')
        query (string): El query en formato SQL
        token (string): El Token de autentificación (SECRET_KEY)
        timeout (float): El número de segundos de espera de los datos antes de dar error. ej 0.2 seg
    """
    ini = time()
    x = requests.get(url, params={'db': db_name, 'q': query, 'token': token}, timeout=timeout)
    # print("REQUEST:", x.json()['query'])
    # {'db': db_name, 'query': query, 'result': result_code, 'datos': datos, '_cuantos': len(datos)}
    rows = x.json()['datos']
    rows_obj = convert_to_obj(rows) if rows else []
    return rows, rows_obj


