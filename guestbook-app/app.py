from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Almacenamiento en memoria
mensajes = []
contador_id = 1

# Ruta principal: muestra la web
@app.route('/')
def index():
    return render_template('index.html')

# GET: lista todos los mensajes
@app.route('/mensajes', methods=['GET'])
def obtener_mensajes():
    return jsonify(mensajes)

# GET: obtiene mensaje por id
@app.route('/mensajes/<int:id>', methods=['GET'])
def obtener_mensaje(id):
    for mensaje in mensajes:
        if mensaje['id'] == id:
            return jsonify(mensaje)
    return jsonify({'error': 'Mensaje no encontrado'}), 404

# POST: agrega nuevo mensaje
@app.route('/mensajes', methods=['POST'])
def crear_mensaje():
    global contador_id
    datos = request.get_json()
    nuevo = {
        'id': contador_id,
        'nombre': datos.get('nombre'),
        'mensaje': datos.get('mensaje')
    }
    mensajes.append(nuevo)
    contador_id += 1
    return jsonify(nuevo), 201

# PUT: actualiza un mensaje
@app.route('/mensajes/<int:id>', methods=['PUT'])
def actualizar_mensaje(id):
    datos = request.get_json()
    for mensaje in mensajes:
        if mensaje['id'] == id:
            mensaje['nombre'] = datos.get('nombre', mensaje['nombre'])
            mensaje['mensaje'] = datos.get('mensaje', mensaje['mensaje'])
            return jsonify(mensaje)
    return jsonify({'error': 'Mensaje no encontrado'}), 404

# DELETE: elimina un mensaje
@app.route('/mensajes/<int:id>', methods=['DELETE'])
def eliminar_mensaje(id):
    for mensaje in mensajes:
        if mensaje['id'] == id:
            mensajes.remove(mensaje)
            return jsonify({'mensaje': 'Mensaje eliminado'})
    return jsonify({'error': 'Mensaje no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)