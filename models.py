from pydantic import BaseModel
from typing import Literal, Optional

class Position(BaseModel):
    x: float
    y: float
    z: float

class Orientation(BaseModel):
    x: float
    y: float
    z: float
    w: float

class TelemetrySnapshot(BaseModel):
    # Identity / context
    inspection_id: str
    inspection_mode: Literal["SCAN", "FOCUS", "IDLE", "CALIBRATE"]
    site_name: str
    asset_id: str
    duct_section: str

    # Environment / sensors (Upgraded High-Fidelity Data)
    internal_temp_c: float
    ambient_temp_c: float
    humidity_pct: float
    particulate_pm25: float
    voc_index: float # Volatile Organic Compounds
    mold_probability_pct: float # AI predicted mold risk
    aqi_score: int # Air Quality Index 0-500
    airflow_mps: float
    static_pressure_pa: float

    # Robot / power / motion
    battery_pct: float
    motor_current_a: float
    vibration_mm_s: float
    signal_strength: float # 0 to 1
    heading_deg: float
    tilt_deg: float
    robot_speed_mps: float
    distance_travelled_m: float

    # 3D Spatial Context (CRITICAL for Dashboard 3D Map Overlay)
    position: Position
    orientation: Orientation

    # Inspection / risk (display)
    last_finding_type: Optional[str]
    risk_score: float
    risk_band: Literal["LOW", "MED", "HIGH"]
    recommended_action: str

    # Time
    timestamp_ms: int

class Finding(BaseModel):
    id: str
    type: str
    severity: Literal["info", "watch", "alert"]
    confidence_pct: float
    duct_offset_m: float
    location: Position # So the frontend can draw a 3D icon right on the 3D WebGL map!
    note: str
    at_ms: int

class ChartPoint(BaseModel):
    t: int # time (epoch ms)
    battery_pct: float
    temp_c: float # maps to internal temp
    vibration: float
    airflow: float
    current: float # motor current
    aqi_score: int 

class NavigationState(BaseModel):
    timestamp_ms: int
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
