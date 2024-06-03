# Wrapper para hacer las conexiones y consultas con las bases de datos de telematel
# tlmplus, tlmplus1, tlmplus2
# Si tenemos acceso directo a través de ODBC pues por ahí que es más rápido.
# en otro caso vía web requests > get_query_pasarela
import pyodbc
from dbTelematelAPI import get_query_pasarela

class ConexionTelematel:
    def __init__(self, connection_string:str="", forzar_pasarela:bool=False, secret_key:str="", url:str=""):
        # Recoger parámetros
        self.token = secret_key
        self.url = url

        # El formato de connection_string es: "DSN=tlmplus;UID=userSQL;PWD=userSQL"
        self.dsn = connection_string.split(";")[0][4:] # Será: tlmplus, tlmplus1 o tlmplus2
        # Ver si tenemos instalados los drivers de 'Progress OpenEdge 10.1B driver'
        data_sources = pyodbc.dataSources()
        # Si usamos 'pypyodbc' las claves del diccionario retornado son bytes b'' y por eso
        # tenemos que decodificarlo en cadenas de texto
        try:
            data_sources_text = {key.decode('utf-8'): value for key, value in data_sources.items()}
        except:
            data_sources_text = data_sources
        
        self.tipo = "odbc" if self.dsn in data_sources_text else "pasarela"
        
        self.tipo = "pasarela" if forzar_pasarela else self.tipo
        
        print(f"CONEXIÓN: {self.tipo} DSN: {self.dsn}")
        
        if self.tipo == "odbc":
            # Primero probamos por odbc, si dá error, pues pasamos a pasarela
            try:
                self.connection = pyodbc.connect(connection_string)
            except:
                self.connection = None
                self.tipo = "pasarela"
        else:
            self.connection = None


    def execute_query(self, query):
        if self.tipo == "odbc":
            # print("Execute: odbc")
            cursor = self.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            rows = [dict(zip([t[0] for t in row.cursor_description], row)) for row in rows] if rows else []
        else:
            # Pues pasarela
            rows, rows_obj = get_query_pasarela(
                self.url,
                db_name=self.dsn,
                query=query,
                token=self.token,
                timeout=30)
            
        return rows

    def close(self):
        # Para cerrar la conexión si es tipo ODBC
        if hasattr(self, 'connection') and self.connection:
            try:
                self.connection.close()
            except pyodbc.ProgrammingError:
                # Ignorar el error si ya está cerrada
                pass

    def __del__(self):
        # Cuando se destruye el objeto llamamos a close() por si acaso.
        self.close()



