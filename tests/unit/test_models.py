"""Tests for Zurichsee models."""

from datetime import datetime

from custom_components.zurichsee_ha.models import MeasurementData, MeasurementResponse


def test_measurement_data_instantiation() -> None:
    """Test MeasurementData model."""
    data = MeasurementData(air_temperature=15.5, timestamp_cet=datetime.now())
    assert data.air_temperature == 15.5
    assert isinstance(data.timestamp_cet, datetime)


def test_measurement_response_parsing() -> None:
    """Test parsing of API response envelope."""
    data = {
        "ok": True,
        "result": [
            {
                "station": "mythenquai",
                "timestamp": "2026-04-29T03:20:00.000Z",
                "values": {"air_temperature": {"value": 15.5, "unit": "°C", "status": "ok"}},
            }
        ],
    }
    model = MeasurementResponse.model_validate(data)
    assert model.ok is True
    assert len(model.result) == 1
    assert model.result[0].values["air_temperature"].value == 15.5
