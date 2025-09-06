def preprocess_image(image):
    '''takes an image file and preprocesses it for OCR'''

    return 

def detect_barcode(image):
    '''detects a barcode in the image'''
    return

def barcode_info(image):
    '''extracts barcode information from the image'''
    return

def ocr_label(image):
    '''performs OCR on the label of the product in the image'''
    return

def process_image(image):
    image = preprocess_image(image)
    if detect_barcode(image):
        return barcode_info(image)
    else:
        return ocr_label(image)

def bad_image(func):
    '''bad image error handling'''
    return "Need Better Image"
