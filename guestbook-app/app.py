from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('guestbook.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/messages', methods=['GET'])
def get_messages():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY timestamp DESC').fetchall()
    conn.close()
    return jsonify([dict(msg) for msg in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    name = data.get('name')
    message = data.get('message')
    if not name or not message:
        return jsonify({'error': 'Name and message are required'}), 400
    conn = get_db_connection()
    conn.execute('INSERT INTO messages (name, message) VALUES (?, ?)', (name, message))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Message created successfully'}), 201

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM messages WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Message deleted successfully'})

@app.route('/messages/<int:id>', methods=['PUT'])
def update_message(id):
    data = request.get_json()
    name = data.get('name')
    message = data.get('message')
    conn = get_db_connection()
    conn.execute('UPDATE messages SET name = ?, message = ? WHERE id = ?', (name, message, id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Message updated successfully'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)