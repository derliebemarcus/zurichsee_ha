"""Tests for Zurichsee API client."""

import json

import aiohttp
import pytest
from aioresponses import aioresponses

from custom_components.zurichsee_ha.api import ZurichseeApiClient
from custom_components.zurichsee_ha.exceptions import ZurichseeApiError


@pytest.mark.asyncio
async def test_async_get_measurements_success() -> None:
    """Test successful data retrieval."""
    with open("tests/fixtures/mythenquai.json") as f:
        mock_data = json.load(f)

    with aioresponses() as m:
        m.get(
            "https://tecdottir.herokuapp.com/measurements/mythenquai?limit=1&sort=timestamp_cet+desc",
            status=200,
            payload=mock_data,
        )

        async with aiohttp.ClientSession() as session:
            client = ZurichseeApiClient(session)
            result = await client.async_get_measurements("mythenquai")

            assert result is not None
            assert result.air_temperature == 12.5
            assert result.water_temperature == 11.2
            assert result.wind_direction == 240


@pytest.mark.asyncio
async def test_async_get_measurements_error() -> None:
    """Test API error handling."""
    with aioresponses() as m:
        m.get(
            "https://tecdottir.herokuapp.com/measurements/mythenquai?limit=1&sort=timestamp_cet+desc",
            status=500,
        )

        async with aiohttp.ClientSession() as session:
            client = ZurichseeApiClient(session)
            with pytest.raises(ZurichseeApiError):
                await client.async_get_measurements("mythenquai")


@pytest.mark.asyncio
async def test_async_validate_connection() -> None:
    """Test connection validation."""
    with open("tests/fixtures/mythenquai.json") as f:
        mock_data = json.load(f)

    with aioresponses() as m:
        m.get(
            "https://tecdottir.herokuapp.com/measurements/mythenquai?limit=1&sort=timestamp_cet+desc",
            status=200,
            payload=mock_data,
        )

        async with aiohttp.ClientSession() as session:
            client = ZurichseeApiClient(session)
            # Should not raise
            await client.async_validate_connection()
