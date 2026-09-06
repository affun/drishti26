from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="DRISHTI API",
    version="1.0.0",
)

# Allow the Next.js development server to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/status")
def get_status():
    return {
        "running": False,
        "camera": "CAM-01",
        "camera_status": "offline",
        "people_detected": 0,
        "zone_status": "secure",
        "active_alerts": 0,
        "fps": 0,
    }


