# Air-Audit System Specification

## Overview
Air-Audit is a data ingestion and distribution pipeline. It acts as the bridge between the robot (currently simulated via the SubPipe dataset) and the frontend dashboard (built externally by another developer).

## Architecture
- **Framework:** FastAPI (Python)
- **Robot Authentication:** Pre-shared static API Keys (Hardware Handshake)
- **Client Authentication:** Simple JWT (Single Admin Login)
- **Data Source (Proxy):** SubPipe (Visual SLAM point clouds `*.ply`, and telemetry aliasing).

## Frontend Data Contracts (The "Dashboard API")

The frontend developer will consume the following endpoints and JSON payloads from our FastAPI backend to populate their UI components:

### 1. `GET /api/v1/telemetry/latest`
**Purpose:** Provides real-time environmental data for the dashboard.
**Payload:**
```json
{
  "timestamp": "2026-03-21T21:40:00Z",
  "temperature_celsius": 22.4, // Mapped from SubPipe Temperature.csv
  "pressure_psi": 14.7, // Mapped from SubPipe Pressure.csv
  "airflow_velocity": 1.2 // Mapped from SubPipe WaterVelocity.csv
}
```

### 2. `GET /api/v1/navigation/state`
**Purpose:** Provides the robot's current position and orientation in the duct.
**Payload:**
```json
{
  "timestamp": "2026-03-21T21:40:00Z",
  "position": {"x": 10.5, "y": 2.1, "z": 0.0},
  "orientation": {"x": 0.0, "y": 0.0, "z": 0.707, "w": 0.707},
  "status": "MOVING" // State enum: "MOVING", "STUCK"
}
```

### 3. `GET /api/v1/map/latest`
**Purpose:** Provides the visual data (3D point cloud and 2D camera images) for the 3D viewer.
**Payload:**
```json
{
  "point_cloud_url": "https://storage.provider/air-audit/maps/chunk0_slam.ply",
  "rgb_image_url": "https://storage.provider/air-audit/images/cam0_latest.jpg"
}
```

### 4. `GET /api/v1/events/poll` (or WebSocket)
**Purpose:** A "ping feature" allowing the app to know immediately if the robot gets stuck so manual override can begin.
**Payload (When stuck):**
```json
{
  "event_type": "ROBOT_STUCK",
  "message": "Robot has encountered an obstruction.",
  "location": {"x": 10.5, "y": 2.1, "z": 0.0}
}
```
