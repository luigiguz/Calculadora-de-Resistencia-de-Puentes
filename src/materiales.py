import json
from db_config import conectar_bd

# Función para insertar un material
def insertar_material(nombre, resistencia_traccion, modulo_elasticidad, densidad):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    query = """
        INSERT INTO materiales (nombre, resistencia_traccion, modulo_elasticidad, densidad)
        VALUES (%s, %s, %s, %s);
    """
    cursor.execute(query, (nombre, resistencia_traccion, modulo_elasticidad, densidad))
    conexion.commit()

    # Resultado del insert en formato JSON, pero ahora lo devolvemos como un diccionario
    resultado = {
        "nombre_material": nombre,
        "resistencia_traccion": str(resistencia_traccion),  # Convertir a string
        "modulo_elasticidad": str(modulo_elasticidad),  # Convertir a string
        "densidad": str(densidad),  # Convertir a string
        "mensaje": f"Material '{nombre}' agregado con éxito."
    }

    cursor.close()
    conexion.close()

    # Imprimir el resultado en consola en formato JSON
    print(json.dumps(resultado, indent=4))

    # Devolver el resultado como un diccionario directamente
    return resultado  # Ahora devuelve un diccionario

# Función para listar los materiales
def listar_materiales():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM materiales;")
    materiales = cursor.fetchall()

    # Lista de materiales
    resultados = []
    for material in materiales:
        id_material, nombre, resistencia_traccion, modulo_elasticidad, densidad = material
        resultado = {
            "id_material": id_material,
            "nombre": nombre,
            "resistencia_traccion": str(resistencia_traccion),  # Convertir a string
            "modulo_elasticidad": str(modulo_elasticidad),  # Convertir a string
            "densidad": str(densidad),  # Convertir a string
        }
        resultados.append(resultado)

    cursor.close()
    conexion.close()

    # Imprimir los resultados en consola en formato JSON
    print(json.dumps(resultados, indent=4))

    # Devolver la lista de resultados como un array (lista de diccionarios)
    return resultados  # Ahora devuelve la lista directamente
