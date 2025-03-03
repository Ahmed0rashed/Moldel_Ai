from fastapi import FastAPI,  File
from fastapi import  Query 
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from fastapi import FastAPI,  File
from fastapi import  Query 
from fastapi.middleware.cors import CORSMiddleware
import os


os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dicom-file-git-main-ahmed0rasheds-projects.vercel.app",
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "capacitor://localhost",
        "app://.",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_EXTENSIONS = {'dcm'}

model = joblib.load("naive_bayes_model.pkl")
tfidf = joblib.load("tfidf_vectorizer.pkl")


class MedicalData(BaseModel):
    modality: str
    body_part_examined: str
    description: str


@app.post("/predict/")
def predict_specialty(data: MedicalData):

    combined_text = f"{data.modality} {data.body_part_examined} {data.description}"
    

    X_new = tfidf.transform([combined_text])
    

    prediction = model.predict(X_new)
    

    return {"Predicted Specialty": prediction[0]}

