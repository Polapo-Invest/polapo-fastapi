from fastapi import FastAPI

# fastapi
app = FastAPI()

@app.get("/")
def test():
    pass