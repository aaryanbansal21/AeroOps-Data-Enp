from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class Position(BaseModel):
    x: float
    y: float
    z: float

class Orientation(BaseModel):
    x: float
    y: float
    z: float
    w: float

class TelemetryResponse(BaseModel):
    timestamp: datetime
    temperature_celsius: float
    pressure_psi: float
    airflow_velocity: float

class NavigationState(BaseModel):
    timestamp: datetime
    position: Position
    orientation: Orientation
    status: Literal["MOVING", "STUCK"]

class MapResponse(BaseModel):
    point_cloud_url: str
    rgb_image_url: str

class EventResponse(BaseModel):
    event_type: Literal["ROBOT_STUCK"]
    message: str
    location: Position
