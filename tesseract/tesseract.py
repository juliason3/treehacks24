import cv2
import pytesseract
from fuzzywuzzy import fuzz
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
    chemicals = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            chemicals.append(row[1].lower())  # Convert to lowercase for case-insensitive comparison
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
def extract_specific_words(text):
    ingredients_section = False
    ingredients = []

    # Join lines with hyphenated words to handle split words
    text_lines = text.split('\n')
    for i in range(len(text_lines) - 1):
        if text_lines[i].endswith('-'):
            text_lines[i] = text_lines[i][:-1] + text_lines[i+1]
            text_lines[i+1] = ''

    for line in text_lines:
        # Check for active ingredients section
        if fuzz.partial_ratio(line.lower(), 'ingredient') >= 70:
            ingredients_section = True
            continue

        # Extract words from active ingredients section
        if ingredients_section:
            ingredients.extend(line.split())

    return ingredients


# Store ingredients in the database
def store_data(ingredients, rating, warning):
    try:
        for ingredient in ingredients:
            cursor.execute("INSERT INTO ingredients (ingredient_name, rating, warning) VALUES (?, ?, ?)", (ingredient, rating, warning))
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
    image_path = "C:\\Users\\vijdi\\OneDrive\\Desktop\\CSProjects\\sunscreenify\\treehacks24\\tesseract\\lacolors.webp"
    text = extract_text(image_path)

    # Extract ingredients from text
    ingredients = extract_specific_words(text)
    if ingredients:
        # Compare extracted ingredients with chemical ingredients
        matching_ingredients = [ingredient for ingredient in ingredients if any(fuzz.partial_ratio(ingredient.lower(), chemical.lower()) >= 70 for chemical in chemical_ingredients)]

        # Store matching ingredients in the database
        if matching_ingredients:
            # Find corresponding rating and warning for each ingredient from the CSV
            with open("C:\\Users\\vijdi\\OneDrive\\Desktop\\CSProjects\\sunscreenify\\treehacks24\\tesseract\\safetydata.csv", newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['Ingredient'].lower() in matching_ingredients:
                        store_data([row['Ingredient']], row['Rating'], row['Warning'])

# Close the cursor and connection
cursor.close()
connection.close()
