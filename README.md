<p align="center">
  <img src="https://raw.githubusercontent.com/derliebemarcus/zurichsee_ha/refs/heads/main/custom_components/zurichsee_ha/brand/logo.png" alt="Zürichsee Wetterstationen Logo" width="200">
</p>

# Zürichsee Wetterstationen for Home Assistant

[![GitHub Release](https://img.shields.io/github/v/release/derliebemarcus/zurichsee_ha)](https://github.com/derliebemarcus/zurichsee_ha/releases)
[![CI](https://github.com/derliebemarcus/zurichsee_ha/actions/workflows/ci.yml/badge.svg)](https://github.com/derliebemarcus/zurichsee_ha/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/derliebemarcus/zurichsee_ha)](LICENSE)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/)
[![Coverage Status](https://img.shields.io/coverallsCoverage/github/derliebemarcus/zurichsee_ha?branch=main&style=for-the-badge)](https://coveralls.io/github/derliebemarcus/zurichsee_ha)

Home Assistant custom integration for weather stations of the Wasserschutzpolizei Zurich (tecdottir API).

## Features

- **Modern UI**: Uses advanced selectors for easy configuration.

- Real-time weather data from **Mythenquai** and **Tiefenbrunnen**.
- Configurable update intervals (15, 30, or 60 minutes).
- Detailed sensors for:
  - Air & Water Temperature
  - Wind Speed, Gusts & Direction
  - Humidity & Dew Point
  - Barometric Pressure (QFE, QFF, QNH)
  - Precipitation & Type
  - Global Radiation
- Fully localizable (English and German supported).

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance.
2. Go to **Integrations** -> **Three dots menu** -> **Custom repositories**.
3. Add `https://github.com/derliebemarcus/zurichsee_ha` with category `Integration`.
4. Search for "Zürichsee Wetterstationen" and click **Install**.
5. Restart Home Assistant.

### Manual

1. Download the latest release.
2. Copy the `custom_components/zurichsee_ha` folder to your Home Assistant `custom_components` directory.
3. Restart Home Assistant.

## Configuration

1. In Home Assistant, go to **Settings** -> **Devices & Services**.
2. Click **Add Integration** and search for **Zürichsee Wetterstationen**.
3. Select the stations you want to monitor and the desired update interval.

## Data Source

This integration uses the [tecdottir API](https://tecdottir.herokuapp.com/docs/) which provides data from the weather stations of the Wasserschutzpolizei Zurich.

- [Tiefenbrunnen Station Info](https://www.tecson-data.ch/zurich/tiefenbrunnen/index.php)
- [Mythenquai Station Info](https://www.tecson-data.ch/zurich/mythenquai/index.php)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
