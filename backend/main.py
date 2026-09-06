import asyncio

import cv2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from detector import DrishtiDetector
from state import STATE

app = FastAPI(
    title="DRISHTI API",
    version="1.0.0",
)

detector = DrishtiDetector()

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
    with STATE.lock:
        return {
            "running": STATE.running,
            "camera": STATE.camera_source,
            "camera_status": STATE.camera_status,
            "people_detected": STATE.people_detected,
            "people_in_zone": STATE.people_in_zone,
            "zone_status": (
                "alert"
                if STATE.people_in_zone > 0
                else "secure"
            ),
            "active_alerts": STATE.alert_count,
            "fps": 0,
        }

@app.post("/api/surveillance/start")
def start_surveillance(source: str = "test.mp4"):
    detector.start(source)

    return {
        "success": True,
        "message": "Surveillance started",
        "source": source,
    }

@app.post("/api/surveillance/stop")
def stop_surveillance():
    detector.stop()

    return {
        "success": True,
        "message": "Surveillance stopped",
    }

def generate_frames():
    while True:
        with STATE.lock:
            frame = STATE.frame

        if frame is None:
            continue

        success, buffer = cv2.imencode(".jpg", frame)

        if not success:
            continue

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes
            + b"\r\n"
        )


@app.get("/api/video")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )