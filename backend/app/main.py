# main.py
from fastapi import FastAPI
from routes import router  # Make sure file is named routes.py and in the same folder
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DreamForge Backend")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routes
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "DreamForge backend is running successfully 🚀"}
