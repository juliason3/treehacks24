import cv2
import pytesseract
from fuzzywuzzy import fuzz
import pandas as pd
import sqlite3
import csv

# Connect to the SQLite database
connection = sqlite3.connect("safety_database.db")
cursor = connection.cursor()

# Create a table to store ingredients if it doesn't exist
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY,
            ingredient_name TEXT NOT NULL,
            rating TEXT NOT NULL,
            warning TEXT NOT NULL
        )
    """)
    print("Table 'ingredients' created successfully")
except sqlite3.Error as err:
    print(f"Error creating table: {err}")

# Function to load chemical ingredients from CSV
def load_chemicals_from_csv(filename):
    chemicals = pd.read_csv(filename)
    chemicals['Ingredient'] = chemicals['Ingredient'].str.lower()  # Convert to lowercase for case-insensitive comparison
    return chemicals

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
def extract_specific_words(text, chemical_ingredients):
    ingredients = []
    for word in text.split():
        word_lower = word.lower()
        best_match = chemical_ingredients[chemical_ingredients['Ingredient'].apply(lambda x: fuzz.partial_ratio(word_lower, x)) >= 90]
        if not best_match.empty:
            ingredients.append(best_match.iloc[0])
    return ingredients

# Calculate the overall percentage based on ratings
def calculate_overall_percentage(ingredients):
    bad_count = sum(1 for ingredient in ingredients if ingredient['Rating'] == "Bad")
    worst_count = sum(2 for ingredient in ingredients if ingredient['Rating'] == "Worst")
    overall_percentage = ((100 - (bad_count) - (worst_count)))
    return overall_percentage

# Store ingredients in the database
def store_data(ingredients, rating, warning):
    try:
        for ingredient in ingredients:
            cursor.execute("INSERT INTO ingredients (ingredient_name, rating, warning) VALUES (?, ?, ?)", (ingredient['Ingredient'], rating, warning))
        connection.commit()
        print("Ingredients stored successfully")
    except sqlite3.Error as err:
        print(f"Error storing data: {err}")
        connection.rollback()

# Example usage
if __name__ == "__main__":
    # Load chemical ingredients from CSV
    chemical_ingredients = load_chemicals_from_csv("C:\\Users\\vijdi\\OneDrive\\Desktop\\CSProjects\\sunscreenify\\treehacks24\\tesseract\\safetydata.csv")

    # Extract text from image
    image_path = "C:\\Users\\vijdi\\OneDrive\\Desktop\\CSProjects\\sunscreenify\\treehacks24\\tesseract\\goodsense.jpg"
    text = extract_text(image_path)
    print("Extracted Text:")
    print(text)

    # Extract ingredients from text
    ingredients = extract_specific_words(text, chemical_ingredients)
    print("Extracted Ingredients:")
    print(ingredients)
    
    if ingredients:
        # Store matching ingredients in the database
        store_data(ingredients, rating="N/A", warning="N/A")

    # Display overall percentage
    if not ingredients:
        print("No ingredients extracted.")
    else:
        overall_percentage = calculate_overall_percentage(ingredients)
        print("Overall Percentage:", overall_percentage)

# Close the cursor and connection
cursor.close()
connection.close()
