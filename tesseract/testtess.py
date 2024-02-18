
import pytesseract
import cv2
def extract_text(image_path):
    print("Image Path:", image_path)  # Print the image path
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(threshold_img)
    return text

image_path = "C:\\Users\\vijdi\\OneDrive\\Desktop\\CSProjects\\sunscreenify\\treehacks24\\tesseract\\active1.jpg"
print(extract_text(image_path))
