import cv2
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
from transformers import pipeline

# Load the AI model (Vision Transformer)
# This is the 'Brain' of your backend
pipe = pipeline("image-classification", model="dima806/deepfake_vs_real_image_detection")

def get_analysis(image_path):
    # 1. AI Pixel Analysis
    raw_result = pipe(image_path)
    ai_verdict = raw_result[0]['label']
    ai_score = raw_result[0]['score']

    # 2. Metadata Check (Cybersecurity Role)
    img = Image.open(image_path)
    exif = img.getexif()
    software = "Original/Unknown"
    is_edited = False
    
    if exif:
        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "Software":
                software = value
                is_edited = True

    # 3. Frequency Artifacts (Deepfake 'Noise' Check)
    # Fakes often have weird patterns in the Fourier Transform
    cv_img = cv2.imread(image_path, 0)
    dft = np.fft.fft2(cv_img)
    dft_shift = np.fft.fftshift(dft)
    magnitude_spectrum = 20 * np.log(np.abs(dft_shift))
    noise_level = np.mean(magnitude_spectrum)

    return {
        "ai_verdict": ai_verdict,
        "ai_confidence": ai_score,
        "software": software,
        "is_edited": is_edited,
        "noise_score": noise_level
    }
