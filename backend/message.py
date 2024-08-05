from flask import Blueprint, request, jsonify
from database import get_db
from model import generate_text

message_bp = Blueprint('message_bp', __name__)

@message_bp.route('/messages', methods=['GET'])
def get_messages():
    chat_id = request.args.get('chat_id')
    if not chat_id:
        return jsonify({"error": "chat_id parameter is required"}), 400

    db = get_db()
    cursor = db.cursor()

    # Get the chat name
    cursor.execute('SELECT name, max_token, temperature FROM chat WHERE id = ?', (chat_id,))
    chat = cursor.fetchone()
    if not chat:
        return jsonify({"error": "Chat not found"}), 404

    # Get the messages
    cursor.execute('SELECT * FROM message WHERE chat_id = ? ORDER BY id', (chat_id,))
    messages = cursor.fetchall()

    return jsonify({
        "chat_id": chat_id,
        "infos": {
            "name": chat[0],
            "max_token": chat[1],
            "temperature": chat[2]
        },
        "messages": [dict(message) for message in messages]
    })

@message_bp.route('/generate', methods=['POST'])
def generate():
    data = request.json
    
    # Extract chat_id, messages, max_new_tokens, and temperature from the request
    chat_id = data.get('chat_id')
    messages = data.get('messages', [])
    max_new_tokens = data.get('max_new_tokens', 100)
    temperature = data.get('temperature', 0.7)
    
    # Extract the last message from the messages list
    if messages:
        last_message = messages[-1]
        last_message_role = last_message['role']
        last_message_content = last_message['content']
    else:
        return jsonify({"error": "Messages list is empty"}), 400
    
    # Insert the last message into the database
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO message (chat_id, role, content)
        VALUES (?, ?, ?)
    ''', (chat_id, last_message_role, last_message_content))
    # last_message_id = cursor.lastrowid
    
    # Generate response based on messages
    generated_text = generate_text(messages, max_new_tokens, temperature)
    
    # Insert the generated message into the database
    cursor.execute('''
        INSERT INTO message (chat_id, role, content)
        VALUES (?, ?, ?)
    ''', (chat_id, 'assistant', generated_text))
    generated_message_id = cursor.lastrowid
    db.commit()
    
    # Construct the response
    response = {
        "chat_id": chat_id,
        "content": generated_text,
        "id": generated_message_id,
        "role": "assistant"
    }
    
    # Return the generated text as a JSON response
    return jsonify(response)