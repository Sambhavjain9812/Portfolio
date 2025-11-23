from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Laundromat API is running ✅"}
