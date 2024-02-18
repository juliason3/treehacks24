from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from PIL import Image
import pytesseract
import io

SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db' #MAKE SURE TO CHANGE THIS TO ACTUALL PATH 
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask application configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your-database-name.db'  # Specify your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# Image upload and text extraction route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    if file:
        img = Image.open(io.BytesIO(file.read()))
        text = pytesseract.image_to_string(img)
        
        # Here you can add the text extraction result to the database
        # For example, if you have a model for storing the results

        return jsonify(text=text), 200

# User registration route
@app.route('/register', methods=['GET', 'POST'])  # Consider using POST for actual registration
def register():
    # Example user - you would use form data in a real application
    new_user = User(username='john doe', email='john@example.com')
    db.session.add(new_user)
    db.session.commit()
    return 'User registered successfully!'

# Home route
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)
