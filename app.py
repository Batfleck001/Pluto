from fastapi import FastAPI
import routes.api as api
import uvicorn

app =  FastAPI()

app.include_router(api.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
