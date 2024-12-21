from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello_world()-> dict[str, str]:
    return {"message": "Hola barcelona!"}
