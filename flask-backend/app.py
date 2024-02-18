from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import io
import os

print("hello")
# Assume we're using the following structure for the FormData:
# skinType: str, skinTone: str, skinConditions: list, image: file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = '/Users/kyliebach/treehacks24/upload'  # Configure this

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model to store user form data
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skinType = db.Column(db.String(50))
    skinTone = db.Column(db.String(50))
    skinConditions = db.Column(db.String(200))  # Comma-separated list
    imagePath = db.Column(db.String(200))  # Path to the image


# Function to save image and return path
def save_image(file):
    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return filepath

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if there is a file in the request
    if 'image' not in request.files:
        return jsonify(error="No image file part"), 400
    image = request.files['image']
    
    # Validate the file is not empty
    if image.filename == '':
        return jsonify(error="No selected file"), 400
    
    # Save the image and get its path
    image_path = save_image(image)
    
    # Process the text fields from the form
    skinType = request.form.get('skinType')
    skinTone = request.form.get('skinTone')
    # Assuming skinConditions are sent as multiple form fields with the same name
    skinConditions = request.form.getlist('skinConditions')  # Returns a list of conditions

    # Create a UserProfile instance
    user_profile = UserProfile(
        skinType=skinType,
        skinTone=skinTone,
        skinConditions=','.join(skinConditions),  # Join the list into a comma-separated string
        imagePath=image_path  # Save the path where the image was saved
    )
    
    # Add the new UserProfile to the session and commit to save to the database
    db.session.add(user_profile)
    db.session.commit()

    # Return a success response
    return jsonify(success=True, profile_id=user_profile.id), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
