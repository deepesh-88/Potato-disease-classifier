from fastapi import FastAPI,File,UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import os

app = FastAPI()

MODEL = tf.keras.models.load_model(r'C:\Users\user\Desktop\All ML projects\potato disease classifier\training\1')
CLASS_NAMES = ["Early Blight" ,"Late Blight","Healthy"]
@app.get("/ping")
async def ping():
    return "hello, I am alive"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())

    image_batch = np.expand_dims(image,0)
    predictions = MODEL.predict(image_batch)
    index = np.argmax(predictions[0])
    predicted_class = CLASS_NAMES[index]
    confidence =np.max(predictions[0])
    return {
        'class':predicted_class,
        'confidence':float(confidence)
    }



