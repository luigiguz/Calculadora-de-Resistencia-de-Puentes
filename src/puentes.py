import json
from db_config import conectar_bd

# Función para insertar un puente
def insertar_puente(nombre, material_id, longitud, ancho, altura, carga_maxima):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    query = """
        INSERT INTO puentes (nombre, material_id, longitud, ancho, altura, carga_maxima)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    cursor.execute(query, (nombre, material_id, longitud, ancho, altura, carga_maxima))
    conexion.commit()

    # Resultado del insert en formato JSON
    resultado = {
        "nombre_puente": nombre,
        "material_id": material_id,
        "longitud": str(longitud),  # Convertir a string
        "ancho": str(ancho),  # Convertir a string
        "altura": str(altura),  # Convertir a string
        "carga_maxima": str(carga_maxima),  # Convertir a string
        "mensaje": f"Puente '{nombre}' agregado con éxito."
    }

    cursor.close()
    conexion.close()

    # Imprimir el resultado en consola en formato JSON
    print(json.dumps(resultado, indent=4))

    # Devolver el resultado como un JSON (aquí también se podría devolver un diccionario si prefieres)
    return resultado  # Ahora devuelve el diccionario directamente

# Función para listar los puentes
def listar_puentes():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT p.id, p.nombre, m.nombre AS material, p.longitud, p.ancho, p.altura, p.carga_maxima
        FROM puentes p
        JOIN materiales m ON p.material_id = m.id;
    """)
    puentes = cursor.fetchall()

    # Lista de puentes
    resultados = []
    for puente in puentes:
        id_puente, nombre, material, longitud, ancho, altura, carga_maxima = puente
        
        # Limpiar caracteres no válidos de 'material'
        material = material.replace("{}", "")  # Eliminar los caracteres '{}' si existen

        # Asegúrate de que el material no tenga caracteres especiales mal formateados
        material = material.encode('utf-8', 'ignore').decode('utf-8')  # Esto debería corregir caracteres extraños

        resultado = {
            "id_puente": id_puente,
            "nombre": nombre,
            "material": material,
            "longitud": str(longitud),  # Convertir a string
            "ancho": str(ancho),  # Convertir a string
            "altura": str(altura),  # Convertir a string
            "carga_maxima": str(carga_maxima),  # Convertir a string
        }
        resultados.append(resultado)

    cursor.close()
    conexion.close()

    # Imprimir los resultados en consola en formato JSON (si quieres mantenerlo)
    print(json.dumps(resultados, indent=4))

    # Devolver la lista de resultados como un array (lista de diccionarios)
    return resultados  # Aquí ya no se usa json.dumps, se devuelve directamente el array
