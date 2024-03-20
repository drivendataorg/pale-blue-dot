from fastapi import FastAPI

app = FastAPI()
app.title = 'Fuegos, una plataforma para conocer el estado del medioambiente'
# app.version = "0.0.1"

@app.get('/', tags=['home'])
def message():
    return 'Hola mundo'