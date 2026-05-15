import io
from io import BytesIO
import time
from PIL import Image
from typing import List, Annotated
from fastapi import FastAPI, File, HTTPException, UploadFile
from model.services import predict, predict_batch as batch_predict
from schemas.schemas import PredictionResult
from model.config import settings

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to the Dog Breed Classification API!"}

@app.get("/model_info")
def model_info():
    return {"model_path": settings.Model_Path, "classes_indices_path": settings.Classes_Indices_Path,"input_size": (150,150)}


@app.post("/single_predict", response_model=PredictionResult)
async def single_predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = Image.open(BytesIO(contents)).convert("RGB")

        start = time.time()
        result = predict(img)
        end  = time.time()

        return{
            "breed": result["class"],
            "confidence": result["confidence"],
            "dog_info": result["dog_info"],
            "processing_time": round(end - start, 2)
                   
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/predict_batch")
async def predict_batch(files: Annotated[List[UploadFile], File(...,description="Upload multiple images")]):
    
    if len(files) == 0:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    if len(files) > settings.Max_Batch_Size:
        raise HTTPException(status_code=400, detail=f"Batch size exceeds maximum of {settings.Max_Batch_Size}")
    


    images = []
    filenames = []


    try:
        for file in files:
            contents = await file.read()
            img = Image.open(BytesIO(contents)).convert("RGB")
            images.append(img)
            filenames.append(file.filename)

        start = time.time()
        results = batch_predict(images)
        end = time.time()
        return{
            "batch_size": len(files),
            "processing_time":round(end - start, 2),
            "results": [
                {
                    "filename": filenames[i],
                    "class_name": results[i]["class"],
                    "confidence": results[i]["confidence"],
                    "dog_info": results[i]["dog_info"]
                }
                for i in range(len(results))
            ]
        }
    

    except Exception as e:
        raise HTTPException(status_code=500, detail="Batch image processing failed")