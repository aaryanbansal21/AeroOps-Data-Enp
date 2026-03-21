from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from auth import verify_admin
from models import TelemetryResponse, NavigationState, MapResponse, EventResponse
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

@app.get("/api/v1/telemetry/latest", response_model=TelemetryResponse, dependencies=[Depends(verify_admin)])
async def get_telemetry():
    return mock_db.get_telemetry()

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
