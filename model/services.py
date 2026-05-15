import joblib
import numpy as np
from tensorflow.keras.models import load_model
from model.config import settings
from tensorflow.keras.preprocessing import image
from PIL import Image
from api.dog_api import get_breed_info

model = None

def get_model():
    global model
    if model is None:
        try:
            model = load_model(settings.Model_Path)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise RuntimeError("Failed to load model.") from e
    return model

class_names = joblib.load(settings.Classes_Indices_Path)


Threshold = settings.Threshold
Margin = settings.Margin


def predict(img: Image.Image):
    img = img.resize((150,150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)/ 255.0

    model = get_model()
    pred = model.predict(img_array)[0]

    top1 = np.max(pred)
    top2 = np.sort(pred)[-2]
    class_index = np.argmax(pred)

    if top1 < Threshold or (top1 - top2) < Margin:
        return {
            "class": "Unknown",
            "confidence": float(top1),
            "dog_info": None
        }
    
    else:
        breed = class_names[class_index]
        breed = breed.split("-")[-1]
        breed = breed.replace("_", " ").title()
        breed = breed.replace(" Dog", "")
        dog_info = get_breed_info(breed)
        return {
            "class": breed,
            "confidence": float(top1),
            "dog_info": dog_info
        }
    


def predict_batch(images: list ):
    processed = []

    for img in images:
        img = img.resize((150,150))
        img_array = image.img_to_array(img)
        img_array = img_array/ 255.0
        processed.append(img_array)

    batch = np.array(processed)
    model = get_model()
    preds = model.predict(batch)

    results = []
    for pred in preds:
        top1 = np.max(pred)
        top2 = np.sort(pred)[-2]
        class_index = np.argmax(pred)

        if top1 < Threshold or (top1 - top2) < Margin:
            results.append({
                "class": "Unknown",
                "confidence": float(top1),
                "dog_info": None
            })
        else:
            breed = class_names[class_index]
            breed = breed.split("-")[-1]
            breed = breed.replace("_", " ").title()
            dog_info = get_breed_info(breed)
            results.append({
                "class": breed,
                "confidence": float(top1),
                "dog_info": dog_info
            })

    return results
    
