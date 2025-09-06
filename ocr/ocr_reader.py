from PIL import Image
import cv2
import numpy as np
import pyzbar
import requests
import pytesseract

def preprocess_image(image_file):
    '''takes an image file and preprocesses it for OCR'''
    image = Image.open(image_file).convert('RGB')

    bgr_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    
    h, w = gray.shape
    if h < 500 or w < 500:
        gray = cv2.resize(gray, (w*2, h*2), interpolation=cv2.INTER_LINEAR)

  
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

   
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 2
    )

    
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = thresh.shape
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    deskewed = cv2.warpAffine(
        thresh, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )
   
    
    return  deskewed

def detect_barcode(image):
    '''detects a barcode in the image'''
    barcodes = pyzbar.decode(image)
    if not barcodes:
        return None
    return barcodes[0].data.decode("utf-8")
    

def barcode_info(barcode):
    '''extracts barcode information from the image'''
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == 1:
            return data["product"]
    return None

def ocr_label(image):
    '''performs OCR on the label of the product in the image'''
    text = pytesseract.image_to_string(image)

    return text.strip()

#main function to process image
def process_image(image_file):
    image = preprocess_image(image_file)
    if detect_barcode(image):
        return barcode_info(detect_barcode(image))
    text = ocr_label(image)
    if text and len(text) > 5:  # crude check 
        return text
    return bad_image()

#fallback for bad images
def bad_image():
    '''bad image error handling'''
    return "Need Better Image"
