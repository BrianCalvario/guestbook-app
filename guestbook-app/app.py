from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return jsonify([
        {
            'id': msg.id,
            'name': msg.name,
            'message': msg.message,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for msg in messages
    ])

@app.route('/messages/<int:message_id>', methods=['GET'])
def get_message(message_id):
    msg = Message.query.get_or_404(message_id)
    return jsonify({
        'id': msg.id,
        'name': msg.name,
        'message': msg.message,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/messages', methods=['POST'])
def add_message():
    data = request.get_json()
    name = data.get('name')
    message = data.get('message')

    if not name or not message:
        return jsonify({'error': 'Nombre y mensaje son requeridos'}), 400

    print(f"Nuevo mensaje recibido: {name} - {message}")

    try:
        new_message = Message(name=name, message=message)
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'message': 'Mensaje agregado correctamente'}), 201
    except Exception as e:
        print(f"Error al agregar mensaje: {e}")
        return jsonify({'error': 'Error interno'}), 500

@app.route('/messages/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    msg = Message.query.get_or_404(message_id)
    data = request.get_json()
    msg.name = data.get('name', msg.name)
    msg.message = data.get('message', msg.message)
    db.session.commit()
    return jsonify({'message': 'Mensaje actualizado correctamente'})

@app.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    msg = Message.query.get_or_404(message_id)
    db.session.delete(msg)
    db.session.commit()
    return jsonify({'message': 'Mensaje eliminado correctamente'})

if __name__ == '__main__':
    app.run(debug=True)