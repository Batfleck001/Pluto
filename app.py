from fastapi import FastAPI

app =  FastAPI()

@app.get("/")
def chat():
    return {"Hello" : "world"}