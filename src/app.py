from flask import Flask, jsonify, request, render_template
from materiales import insertar_material, listar_materiales
from puentes import insertar_puente, listar_puentes
from calculos import calcular_resistencia, listar_calculos

app = Flask(__name__)

# Ruta principal
@app.route("/")
def inicio():
    return render_template("inicio.html")

# Rutas para gestionar Materiales
@app.route("/materiales")
def inicio_materiales():
    return render_template("inicio_materiales.html")

@app.route("/materiales/agregar")
def agregar_material():
    return render_template("agregar_material.html")

@app.route("/materiales/listar")
def listar_materiales_html():
    return render_template("listar_materiales.html")

@app.route("/api/materiales", methods=["GET", "POST"])
def api_materiales():
    if request.method == "POST":
        data = request.get_json()
        required_keys = ["nombre", "resistencia_traccion", "modulo_elasticidad", "densidad"]
        
        # Verificar parámetros
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            return jsonify({"error": f"Faltan los siguientes parámetros: {', '.join(missing_keys)}"}), 400

        try:
            insertar_material(
                data["nombre"], 
                data["resistencia_traccion"], 
                data["modulo_elasticidad"], 
                data["densidad"]
            )
            return jsonify({"message": "Material agregado exitosamente"}), 201
        except Exception as e:
            return jsonify({"error": f"Error al insertar material: {str(e)}"}), 500

    try:
        materiales = listar_materiales()
        return jsonify(materiales), 200
    except Exception as e:
        return jsonify({"error": f"Error al listar materiales: {str(e)}"}), 500

# Rutas para gestionar Puentes
@app.route("/puentes")
def inicio_puentes():
    return render_template("inicio_puentes.html")

@app.route("/puentes/agregar")
def agregar_puente():
    return render_template("agregar_puente.html")

@app.route("/puentes/listar")
def listar_puentes_html():
    return render_template("listar_puentes.html")

@app.route("/api/puentes", methods=["GET", "POST"])
def api_puentes():
    if request.method == "POST":
        data = request.get_json()
        required_keys = ["nombre", "material_id", "longitud", "ancho", "altura", "carga_maxima"]
        
        # Verificar parámetros
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            return jsonify({"error": f"Faltan los siguientes parámetros: {', '.join(missing_keys)}"}), 400

        try:
            insertar_puente(
                data["nombre"], 
                data["material_id"], 
                data["longitud"], 
                data["ancho"], 
                data["altura"], 
                data["carga_maxima"]
            )
            return jsonify({"message": "Puente agregado exitosamente"}), 201
        except Exception as e:
            return jsonify({"error": f"Error al insertar puente: {str(e)}"}), 500

    try:
        puentes = listar_puentes()
        return jsonify(puentes), 200
    except Exception as e:
        return jsonify({"error": f"Error al listar puentes: {str(e)}"}), 500

# Rutas para cálculos
@app.route("/calculos")
def inicio_calculos():
    return render_template("inicio_calculos.html")

@app.route("/calculos/realizar")
def realizar_calculo():
    return render_template("realizar_calculos.html")

@app.route("/calculos/listar")
def listar_calculos_html():
    return render_template("listar_calculos.html")

@app.route("/api/calcular_resistencia", methods=["POST"])
def api_calcular():
    data = request.get_json()
    required_keys = ["puente_id", "factor_seguridad"]
    
    # Verificar parámetros
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        return jsonify({"error": f"Faltan los siguientes parámetros: {', '.join(missing_keys)}"}), 400

    try:
        resistencia_final = calcular_resistencia(data["puente_id"], data["factor_seguridad"])
        return jsonify({"message": "Cálculo realizado exitosamente", "resistencia_final": resistencia_final}), 200
    except Exception as e:
        return jsonify({"error": f"Error al calcular resistencia: {str(e)}"}), 500

@app.route("/api/calculos", methods=["GET"])
def api_calculos():
    try:
        calculos = listar_calculos()
        return jsonify(calculos), 200
    except Exception as e:
        return jsonify({"error": f"Error al listar cálculos: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
