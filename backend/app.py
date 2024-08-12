from flask import Flask, request
from flask_cors import CORS
from chat import chat_bp
from message import message_bp
from database import init_db, close_db
import os
from dotenv import load_dotenv

load_dotenv()

CORS_ORIGINS = os.getenv('CORS_ORIGINS')

app = Flask(__name__)

# Initialize the database
init_db()

# Register Blueprints
app.register_blueprint(chat_bp)
app.register_blueprint(message_bp)

# Enable CORS
cors = CORS(app, resources={r"/*": {"origins": CORS_ORIGINS}})

# Close the database connection after each request
@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

# Debugging route to check CORS headers
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,UPDATE,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)
