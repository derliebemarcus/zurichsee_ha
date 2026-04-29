"""Tests for Zurichsee models."""

from datetime import datetime

from custom_components.zurichsee_ha.models import MeasurementResponse, MeasurementValues


def test_measurement_values_parsing():
    """Test parsing of measurement values."""
    data = {"air_temperature": 15.5, "timestamp_cet": "2024-04-29T06:00:00+02:00"}
    model = MeasurementValues.model_validate(data)
    assert model.air_temperature == 15.5
    assert isinstance(model.timestamp_cet, datetime)


def test_measurement_response_parsing():
    """Test parsing of API response envelope."""
    data = {"ok": True, "result": [{"air_temperature": 15.5}]}
    model = MeasurementResponse.model_validate(data)
    assert model.ok is True
    assert len(model.result) == 1
    assert model.result[0].air_temperature == 15.5
