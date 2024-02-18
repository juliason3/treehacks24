import cv2
import pytesseract
from fuzzywuzzy import fuzz
import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect("sunscreen.db")
cursor = connection.cursor()

# Create a table to store ingredients if it doesn't exist
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY,
            ingredient_name TEXT NOT NULL
        )
    """)
    print("Table 'ingredients' created successfully")
except sqlite3.Error as err:
    print(f"Error creating table: {err}")

# Set the path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Extract text from image using pytesseract
def extract_text(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(threshold_img)
    return text

# Extract ingredients from text
def extract_specific_words(text):
    ingredients_section = False
    ingredients = []

    for line in text.split('\n'):
        # Check for active ingredients section
        if fuzz.partial_ratio(line.lower(), 'active ingredients') >= 70:
            ingredients_section = True
            continue

        # Extract words from active ingredients section
        if ingredients_section:
            ingredients.extend(line.split())

    return ingredients

# Store ingredients in the database
def store_data(ingredients):
    try:
        for ingredient in ingredients:
            cursor.execute("INSERT INTO ingredients (ingredient_name) VALUES (?)", (ingredient,))
        connection.commit()
        print("Ingredients stored successfully")
    except sqlite3.Error as err:
        print(f"Error storing data: {err}")
        connection.rollback()

# Example usage
if __name__ == "__main__":
    # Extract text from image
    image_path = "neutrogena-01.jpg"
    text = extract_text(image_path)

    # Extract ingredients from text
    ingredients = extract_specific_words(text)

    if ingredients:
        store_data(ingredients)

# Close the cursor and connection
cursor.close()
connection.close()
