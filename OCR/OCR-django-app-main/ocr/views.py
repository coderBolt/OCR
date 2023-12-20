import base64
import numpy as np
import pytesseract
from django.contrib import messages
from django.shortcuts import render
from PIL import Image
from gtts import gTTS
from playsound import playsound
from googletrans import Translator

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Path to tesseract.exe
)

def homepage(request):
    if request.method == "POST":
        try:
            image = request.FILES["imagefile"]
            # encode image to base64 string
            image_base64 = base64.b64encode(image.read()).decode("utf-8")
        except:
            messages.add_message(
                request, messages.ERROR, "No image selected or uploaded"
            )
            return render(request, "home.html")
        lang = request.POST["language"]
        trans_lang = request.POST["language_trans"]
        img = np.array(Image.open(image))
        text = pytesseract.image_to_string(img, lang=lang)
        trans_text = translate_text(text,trans_lang)
        if lang == 'eng':
            tts = gTTS(text=text, lang='en')
            audio_file = 'F:/OCR/OCR-django-app-main/templates/output.mp3'
            tts.save(audio_file)
            playsound(audio_file)
        # return text to html
        return render(request, "home.html", {"ocr": text, "image": image_base64, "trans_text":trans_text})
    
    return render(request, "home.html")

def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    translated_text = translated.text
    return translated_text



