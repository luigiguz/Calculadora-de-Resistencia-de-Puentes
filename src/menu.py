from db_config import conectar_bd
from materiales import insertar_material, listar_materiales
from puentes import insertar_puente, listar_puentes
from calculos import calcular_resistencia, listar_calculos

if __name__ == "__main__":
    while True:
        print("\n--- Menú de Calculadora ---")
        print("1. Insertar material")
        print("2. Listar materiales")
        print("3. Insertar puente")
        print("4. Listar puentes")
        print("5. Calcular resistencia de un puente")
        print("6. Listar cálculos realizados")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre del material: ")
            resistencia_traccion = float(input("Resistencia a la tracción (MPa): "))
            modulo_elasticidad = float(input("Módulo de elasticidad (GPa): "))
            densidad = float(input("Densidad (kg/m³): "))
            insertar_material(nombre, resistencia_traccion, modulo_elasticidad, densidad)
        elif opcion == "2":
            listar_materiales()
        elif opcion == "3":
            nombre = input("Nombre del puente: ")
            material_id = int(input("ID del material: "))
            longitud = float(input("Longitud (m): "))
            ancho = float(input("Ancho (m): "))
            altura = float(input("Altura (m): "))
            carga_maxima = float(input("Carga máxima (toneladas): "))
            insertar_puente(nombre, material_id, longitud, ancho, altura, carga_maxima)
        elif opcion == "4":
            # Listar los puentes por nombre
            listar_puentes()
        elif opcion == "5":
            puente_id = int(input("ID del puente: "))  # Pide el ID del puente
            factor_seguridad = input("Factor de seguridad (default 1.5): ")
            factor_seguridad = float(factor_seguridad) if factor_seguridad else 1.5  # Si no se proporciona, usa el valor por defecto
            calcular_resistencia(puente_id, factor_seguridad)  # Llama a la función con los parámetros correctos
        elif opcion == "6":
            listar_calculos()    
        elif opcion == "7":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")
