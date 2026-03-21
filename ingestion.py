import time
from models import TelemetrySnapshot, NavigationState, Position, Orientation, MapResponse, EventResponse, Finding, ChartPoint
from typing import List

class MockSubPipeData:
    def get_telemetry_snapshot(self) -> TelemetrySnapshot:
        return TelemetrySnapshot(
            inspection_id="INSP-001",
            inspection_mode="SCAN",
            site_name="HVAC Zone Alpha",
            asset_id="DUCT-09A",
            duct_section="Main Intake",
            internal_temp_c=35.2,
            ambient_temp_c=22.4,
            humidity_pct=45.0,
            particulate_pm25=12.5,
            airflow_mps=1.2,
            static_pressure_pa=14.7,
            battery_pct=82.5,
            motor_current_a=2.4,
            vibration_mm_s=0.15,
            signal_strength=0.88,
            heading_deg=180.0,
            tilt_deg=2.5,
            robot_speed_mps=0.5,
            distance_travelled_m=12.0,
            position_m=12.0,
            last_finding_type="Corrosion",
            risk_score=65.0,
            risk_band="MED",
            recommended_action="Schedule maintenance within 30 days.",
            timestamp_ms=int(time.time() * 1000)
        )

    def get_findings(self) -> List[Finding]:
        return [
            Finding(
                id="FIND-001",
                type="Rust Patch",
                severity="alert",
                confidence_pct=92.5,
                duct_offset_m=5.2,
                note="Significant rust progression detected on bottom panel.",
                at_ms=int(time.time() * 1000) - 60000
            ),
            Finding(
                id="FIND-002",
                type="Debris",
                severity="watch",
                confidence_pct=78.0,
                duct_offset_m=8.5,
                note="Minor dust buildup.",
                at_ms=int(time.time() * 1000) - 30000
            )
        ]

    def get_history(self) -> List[ChartPoint]:
        now = int(time.time() * 1000)
        return [
            ChartPoint(t=now - 10000, battery_pct=83.0, temp_c=35.0, vibration=0.1, airflow=1.2, current=2.3),
            ChartPoint(t=now - 5000, battery_pct=82.8, temp_c=35.1, vibration=0.12, airflow=1.2, current=2.4),
            ChartPoint(t=now, battery_pct=82.5, temp_c=35.2, vibration=0.15, airflow=1.2, current=2.4)
        ]

    def get_navigation(self) -> NavigationState:
        return NavigationState(
            timestamp_ms=int(time.time() * 1000),
            position=Position(x=10.5, y=2.1, z=0.0),
            orientation=Orientation(x=0.0, y=0.0, z=0.707, w=0.707),
            status="MOVING"
        )

    def get_map(self) -> MapResponse:
        return MapResponse(
            point_cloud_url="http://127.0.0.1:8000/static/maps/mock_duct.ply",
            rgb_image_url="https://storage.provider/air-audit/images/cam0_latest.jpg"
        )

    def get_event(self) -> EventResponse:
        return EventResponse(
            event_type="ROBOT_STUCK",
            message="Robot has encountered an obstruction.",
            location=Position(x=10.5, y=2.1, z=0.0)
        )

mock_db = MockSubPipeData()
