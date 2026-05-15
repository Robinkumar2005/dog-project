import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    Model_Path = os.getenv("MODEL_PATH", "model/dog_classifier.keras")
    Classes_Indices_Path = os.getenv("CLASSES_INDICES_PATH", "model/classes.pkl")
    Threshold = float(os.getenv("THRESHOLD", 0.6))
    Margin = float(os.getenv("MARGIN", 0.15))
    Max_Batch_Size = int(os.getenv("MAX_BATCH_SIZE", 10))
settings = Settings()
