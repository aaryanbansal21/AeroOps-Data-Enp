# Air-Audit System Specification

## Overview
Air-Audit is a data ingestion and distribution pipeline servicing the frontend dashboard. 

## Frontend Data Contracts (The "Dashboard API")

The frontend developer can access the following 6 endpoints containing strictly typed simulated values:

### 1. `GET /api/v1/telemetry/snapshot`
**Purpose:** Provides the comprehensive real-time robot state, environmental metrics, and inspection context.
**Payload Schema:**
- **Context:** `inspection_id`, `inspection_mode`, `site_name`, `asset_id`, `duct_section`
- **Environment:** `internal_temp_c`, `ambient_temp_c`, `humidity_pct`, `particulate_pm25`, `airflow_mps`, `static_pressure_pa`
- **Robot:** `battery_pct`, `motor_current_a`, `vibration_mm_s`, `signal_strength`, `heading_deg`, `tilt_deg`, `robot_speed_mps`, `distance_travelled_m`, `position_m`
- **Risk:** `last_finding_type`, `risk_score`, `risk_band`, `recommended_action`
- **Time:** `timestamp_ms`

### 2. `GET /api/v1/findings`
**Purpose:** Provides the feed of specific anomalies/alerts detected by the robot (the "feed rows").
**Payload Schema (Array of Objects):**
- `id`, `type`, `severity` (info|watch|alert), `confidence_pct`, `duct_offset_m`, `note`, `at_ms`

### 3. `GET /api/v1/history`
**Purpose:** Time-series history required for drawing the bottom chart.
**Payload Schema (Array of Objects):**
- `t` (epoch ms), `battery_pct`, `temp_c`, `vibration`, `airflow`, `current`

### 4. `GET /api/v1/navigation/state`
**Purpose:** Minimal legacy state containing quaternion `orientation` and `status` ("MOVING" | "STUCK").

### 5. `GET /api/v1/map/latest`
**Purpose:** Provides the visual data for the WebGL 3D viewer.
**Payload Schema:**
- `point_cloud_url` (Serves the synthetic 80k point `.ply` duct file)
- `rgb_image_url`

### 6. `GET /api/v1/events/poll`
**Purpose:** Event polling for emergency physical overrides.
