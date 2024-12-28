#pip install mysql-connector-python

import mysql.connector
from mysql.connector import Error

def conectar_bd():
    try:
        # Intentar conectar a la base de datos
        conexion = mysql.connector.connect(
            host="localhost",        # Cambia esto si tu BD no está en localhost
            user="root",             # Usuario de MySQL
            password="",             # Contraseña de MySQL
            database="calculadora"   # Nombre de la BD
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos.")
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    finally:
        pass
