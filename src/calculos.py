import json
from db_config import conectar_bd
from decimal import Decimal

# Función para calcular la resistencia de un puente
def calcular_resistencia(puente_id, factor_seguridad=1.5):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    query = """
        SELECT p.longitud, p.ancho, p.altura, p.carga_maxima, 
               m.resistencia_traccion, m.modulo_elasticidad
        FROM puentes p
        JOIN materiales m ON p.material_id = m.id
        WHERE p.id = %s;
    """
    cursor.execute(query, (puente_id,))
    puente = cursor.fetchone()

    if not puente:
        # Si no se encuentra el puente, devolver un mensaje de error
        cursor.close()
        conexion.close()
        error_response = {"error": "Puente no encontrado"}
        print(json.dumps(error_response, indent=4))  # Imprimir error en formato JSON
        return error_response  # Devolver el diccionario de error directamente

    longitud, ancho, altura, carga_maxima, resistencia_traccion, modulo_elasticidad = puente
    area_transversal = Decimal(ancho) * Decimal(altura)  # Convertir a Decimal para precisión
    resistencia_teorica = Decimal(resistencia_traccion) * area_transversal
    resistencia_final = resistencia_teorica / Decimal(str(factor_seguridad))  # Conversión a Decimal

    # Insertar el resultado del cálculo en la base de datos
    insert_query = """
        INSERT INTO calculos_resistencia (puente_id, resistencia_calculada, factor_seguridad, resultado_final)
        VALUES (%s, %s, %s, %s);
    """
    cursor.execute(insert_query, (puente_id, resistencia_teorica, factor_seguridad, resistencia_final))
    conexion.commit()

    # Resultado del cálculo en formato JSON (pero lo devolvemos como diccionario)
    resultado = {
        "puente_id": puente_id,
        "resistencia_calculada": str(resistencia_teorica),  # Convertir Decimal a string
        "factor_seguridad": float(factor_seguridad),
        "resistencia_final": str(resistencia_final),  # Convertir Decimal a string
        "mensaje": f"Resistencia calculada para el puente ID {puente_id}"
    }

    cursor.close()
    conexion.close()

    # Imprimir el resultado en consola en formato JSON
    print(json.dumps(resultado, indent=4))

    # Devolver el resultado como un diccionario
    return resultado  # Ahora devuelve el diccionario directamente

# Función para listar los cálculos de resistencia realizados
def listar_calculos():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    # Consultar los cálculos realizados junto con el nombre del puente
    query = """
        SELECT p.nombre, c.resistencia_calculada, c.factor_seguridad, c.resultado_final, c.fecha_calculo
        FROM calculos_resistencia c
        JOIN puentes p ON c.puente_id = p.id;
    """
    
    cursor.execute(query)
    calculos = cursor.fetchall()

    # Lista para almacenar los resultados
    resultados = []
    for calculo in calculos:
        nombre_puente, resistencia_calculada, factor_seguridad, resultado_final, fecha_calculo = calculo
        resultado = {
            "nombre_puente": nombre_puente,
            "resistencia_calculada": str(resistencia_calculada),  # Convertir Decimal a string
            "factor_seguridad": float(factor_seguridad),
            "resultado_final": str(resultado_final),  # Convertir Decimal a string
            "fecha_calculo": str(fecha_calculo)
        }
        resultados.append(resultado)

    cursor.close()
    conexion.close()

    # Imprimir los resultados en consola en formato JSON
    print(json.dumps(resultados, indent=4))

    # Devolver la lista de resultados como un array (lista de diccionarios)
    return resultados  # Ahora devuelve la lista directamente
