from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
import os
from auth import verify_admin
from models import TelemetrySnapshot, NavigationState, MapResponse, EventResponse, Finding, ChartPoint
from ingestion import mock_db
import uvicorn

app = FastAPI(title="Air-Audit Pipeline", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static/maps", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"status": "ok", "message": "Air-Audit API is running! Go to /docs to view the interactive endpoints."}

@app.get("/api/v1/telemetry/snapshot", response_model=TelemetrySnapshot, dependencies=[Depends(verify_admin)])
async def get_telemetry_snapshot():
    """Returns the comprehensive real-time robot state and environmental metrics."""
    return mock_db.get_telemetry_snapshot()

@app.get("/api/v1/findings", response_model=List[Finding], dependencies=[Depends(verify_admin)])
async def get_findings():
    """Returns the feed of specific findings/alerts detected by the robot."""
    return mock_db.get_findings()

@app.get("/api/v1/history", response_model=List[ChartPoint], dependencies=[Depends(verify_admin)])
async def get_history():
    """Returns the time-series history required for drawing the bottom chart."""
    return mock_db.get_history()

@app.get("/api/v1/navigation/state", response_model=NavigationState, dependencies=[Depends(verify_admin)])
async def get_navigation():
    return mock_db.get_navigation()

@app.get("/api/v1/map/latest", response_model=MapResponse, dependencies=[Depends(verify_admin)])
async def get_map():
    return mock_db.get_map()

@app.get("/api/v1/events/poll", response_model=EventResponse, dependencies=[Depends(verify_admin)])
async def poll_events():
    return mock_db.get_event()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
