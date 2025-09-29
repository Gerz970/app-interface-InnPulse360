from fastapi import FastAPI

# Crear instancia de FastAPI
app = FastAPI(title="InnPulse360 API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Bienvenido a InnPulse360 API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)