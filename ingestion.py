import time
import random
from models import TelemetrySnapshot, NavigationState, Position, Orientation, MapResponse, EventResponse, Finding, ChartPoint
from typing import List

class MockSubPipeData:
    def _random_walk(self, base, variance):
        """Simulate real hardware sensor flutter around a baseline target."""
        return round(base + random.uniform(-variance, variance), 2)

    def _current_position(self) -> Position:
        # Simulate the robot slowly traveling securely down the duct's Z axis
        return Position(
            x=self._random_walk(0.0, 0.1),
            y=self._random_walk(0.0, 0.1),
            z=self._random_walk(5.5, 0.5) # Currently 5.5 meters deep into the vent
        )

    def get_telemetry_snapshot(self) -> TelemetrySnapshot:
        return TelemetrySnapshot(
            inspection_id="INSP-001",
            inspection_mode="SCAN",
            site_name="HVAC Zone Alpha",
            asset_id="DUCT-09A",
            duct_section="Main Intake",
            # Fluctuating High-Fidelity Data
            internal_temp_c=self._random_walk(35.2, 0.4),
            ambient_temp_c=self._random_walk(22.4, 0.2),
            humidity_pct=self._random_walk(45.0, 1.5),
            particulate_pm25=self._random_walk(12.5, 0.8),
            voc_index=self._random_walk(4.2, 0.3),                 
            mold_probability_pct=self._random_walk(18.5, 2.0),     
            aqi_score=int(self._random_walk(42, 3)),               
            airflow_mps=self._random_walk(1.2, 0.1),
            static_pressure_pa=self._random_walk(14.7, 0.05),
            # Hardware
            battery_pct=self._random_walk(82.5, 0.1), 
            motor_current_a=self._random_walk(2.4, 0.3),
            vibration_mm_s=self._random_walk(0.15, 0.03),
            signal_strength=self._random_walk(0.88, 0.02),
            heading_deg=self._random_walk(180.0, 1.0),
            tilt_deg=self._random_walk(2.5, 0.1),
            robot_speed_mps=self._random_walk(0.5, 0.05),
            distance_travelled_m=self._random_walk(5.5, 0.02),
            # Exact Spatial Coordinate Mapping for 3D Overlay UX!
            position=self._current_position(),
            orientation=Orientation(x=0.0, y=0.0, z=0.707, w=0.707),
            # ML Risk Values
            last_finding_type=random.choice(["Corrosion", "Mold Spores", None]),
            risk_score=self._random_walk(65.0, 2.0),
            risk_band=random.choice(["LOW", "MED", "MED"]), 
            recommended_action="Schedule maintenance within 30 days.",
            timestamp_ms=int(time.time() * 1000)
        )

    def get_findings(self) -> List[Finding]:
        now = int(time.time() * 1000)
        return [
            Finding(
                id="FIND-001",
                type="Rust Patch",
                severity="alert",
                confidence_pct=92.5,
                duct_offset_m=5.2,
                location=Position(x=-0.8, y=0.0, z=5.2), # Exact 3D map spatial locus
                note="Significant rust progression detected on bottom panel.",
                at_ms=now - 60000
            ),
            Finding(
                id="FIND-002",
                type="Mold Spores",
                severity="watch",
                confidence_pct=88.4,
                duct_offset_m=8.5,
                location=Position(x=0.2, y=0.9, z=8.5), # Exact 3D map spatial locus
                note="High mold probability detected. VOC index elevated globally.",
                at_ms=now - 30000
            )
        ]

    def get_history(self) -> List[ChartPoint]:
        now = int(time.time() * 1000)
        return [
            ChartPoint(t=now - 10000, battery_pct=83.0, temp_c=self._random_walk(35.0, 0.2), vibration=0.1, airflow=self._random_walk(1.2, 0.1), current=2.3, aqi_score=40),
            ChartPoint(t=now - 5000, battery_pct=82.8, temp_c=self._random_walk(35.1, 0.2), vibration=0.12, airflow=self._random_walk(1.2, 0.1), current=2.4, aqi_score=41),
            ChartPoint(t=now, battery_pct=82.5, temp_c=self._random_walk(35.2, 0.2), vibration=0.15, airflow=self._random_walk(1.2, 0.1), current=2.4, aqi_score=42)
        ]

    def get_navigation(self) -> NavigationState:
        return NavigationState(
            timestamp_ms=int(time.time() * 1000),
            position=self._current_position(),
            orientation=Orientation(x=0.0, y=0.0, z=0.707, w=0.707),
            status="MOVING"
        )

    def get_map(self) -> MapResponse:
        return MapResponse(
            point_cloud_url="/static/maps/mock_duct_rect.ply",
            rgb_image_url="https://storage.provider/air-audit/images/cam0_latest.jpg"
        )

    def get_event(self) -> EventResponse:
        return EventResponse(
            event_type="ROBOT_STUCK",
            message="Robot has encountered an obstruction.",
            location=self._current_position()
        )

mock_db = MockSubPipeData()
