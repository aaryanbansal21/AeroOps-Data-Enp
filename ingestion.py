from datetime import datetime, timezone
from models import TelemetryResponse, NavigationState, Position, Orientation, MapResponse, EventResponse

# Simulated state mapped from SubPipe alias datastreams
class MockSubPipeData:
    def get_telemetry(self) -> TelemetryResponse:
        return TelemetryResponse(
            timestamp=datetime.now(timezone.utc),
            temperature_celsius=22.4, # from Temperature.csv
            pressure_psi=14.7,        # from Pressure.csv
            airflow_velocity=1.2      # from WaterVelocity.csv
        )

    def get_navigation(self) -> NavigationState:
        return NavigationState(
            timestamp=datetime.now(timezone.utc),
            position=Position(x=10.5, y=2.1, z=0.0),
            orientation=Orientation(x=0.0, y=0.0, z=0.707, w=0.707),
            status="MOVING"
        )

    def get_map(self) -> MapResponse:
        return MapResponse(
            point_cloud_url="https://storage.provider/air-audit/maps/chunk0_slam.ply",
            rgb_image_url="https://storage.provider/air-audit/images/cam0_latest.jpg"
        )

    def get_event(self) -> EventResponse:
        return EventResponse(
            event_type="ROBOT_STUCK",
            message="Robot has encountered an obstruction.",
            location=Position(x=10.5, y=2.1, z=0.0)
        )

mock_db = MockSubPipeData()
