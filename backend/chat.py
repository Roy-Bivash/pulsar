from flask import Blueprint, request, jsonify
from database import get_db

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/chat', methods=['GET'])
def get_chats():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM chat')
    chats = cursor.fetchall()
    return jsonify([dict(chat) for chat in chats])

@chat_bp.route('/chat', methods=['POST'])
def add_chat():
    new_chat = request.get_json()
    name = new_chat['name']
    prompt = new_chat.get('prompt')

    db = get_db()
    cursor = db.cursor()
    
    # Insert the new chat into the chat table
    cursor.execute('INSERT INTO chat (name, max_token, temperature) VALUES (?, ?, ?)', (name, 200, 0.7))
    chat_id = cursor.lastrowid

    # Insert the prompt into the message table with role "system"
    if prompt:
        cursor.execute('''
            INSERT INTO message (chat_id, role, content)
            VALUES (?, ?, ?)
        ''', (chat_id, 'system', prompt))

    db.commit()
    
    return jsonify(new_chat), 201

@chat_bp.route('/chat/<int:chat_id>', methods=['UPDATE'])
def update_chat(chat_id):
    update_data = request.get_json()
    name = update_data.get('name')
    max_token = update_data.get('max_token')
    temperature = update_data.get('temperature')

    db = get_db()
    cursor = db.cursor()

    # Build the SQL query dynamically based on provided fields
    fields_to_update = []
    values = []

    if name is not None:
        fields_to_update.append('name = ?')
        values.append(name)

    if max_token is not None:
        fields_to_update.append('max_token = ?')
        values.append(max_token)

    if temperature is not None:
        fields_to_update.append('temperature = ?')
        values.append(temperature)

    values.append(chat_id)

    if fields_to_update:
        sql_query = f"UPDATE chat SET {', '.join(fields_to_update)} WHERE id = ?"
        cursor.execute(sql_query, values)
        db.commit()

    return jsonify({"message": "Chat updated successfully"}), 200


@chat_bp.route('/chat/<int:chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    db = get_db()
    cursor = db.cursor()

    # Delete all messages associated with the chat
    cursor.execute('DELETE FROM message WHERE chat_id = ?', (chat_id,))

    # Delete the chat itself
    cursor.execute('DELETE FROM chat WHERE id = ?', (chat_id,))

    db.commit()

    return jsonify({"message": "success"}), 200