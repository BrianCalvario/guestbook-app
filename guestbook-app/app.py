from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'guestbook.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'message': self.message,
            'timestamp': self.timestamp.isoformat()
        }

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return jsonify([msg.to_dict() for msg in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(name=data['name'], message=data['message'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:message_id>', methods=['GET'])
def get_message(message_id):
    msg = Message.query.get(message_id)
    if msg:
        return jsonify(msg.to_dict())
    return jsonify({'error': 'Mensaje no encontrado'}), 404

@app.route('/messages/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    data = request.get_json()
    msg = Message.query.get(message_id)
    if msg:
        msg.name = data.get('name', msg.name)
        msg.message = data.get('message', msg.message)
        db.session.commit()
        return jsonify(msg.to_dict())
    return jsonify({'error': 'Mensaje no encontrado'}), 404

@app.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    msg = Message.query.get(message_id)
    if msg:
        db.session.delete(msg)
        db.session.commit()
        return jsonify({'result': 'Mensaje eliminado'}), 200
    return jsonify({'error': 'Mensaje no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)