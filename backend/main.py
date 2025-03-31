from fastapi import FastAPI

app = FastAPI()

# here
@app.get("/")
async def root():
    return {"message": "Welcome to the Health App!"}
