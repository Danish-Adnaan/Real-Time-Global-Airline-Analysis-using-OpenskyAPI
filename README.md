# Azure Flight Data Ingestion

This Azure Function ingests real-time flight data from OpenSky Network API and streams it to an Azure Event Hub for processing in Microsoft Fabric.


<img width="1129" height="638" alt="image" src="https://github.com/user-attachments/assets/8ed4b2d1-a0a9-4295-ab1f-c93af2d6fd95" />


<img width="1131" height="645" alt="image" src="https://github.com/user-attachments/assets/f7f91e5a-6c46-4420-9ff1-e908e4ca211e" />


## Features

- **Timer-triggered Azure Function** that runs every 4 minutes
- Fetches live flight data from OpenSky Network API
- Enriches flight data with geographical country information
- Streams data to Azure Event Hub for real-time processing
- Handles authentication with OpenSky Network for higher rate limits

## Prerequisites

- Python 3.9 or higher
- Azure subscription
- Azure Event Hub / Microsoft Fabric Event Stream
- OpenSky Network account (optional, for higher API rate limits)

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
# or
source .venv/bin/activate  # On Linux/Mac
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `local.settings.json.example` to `local.settings.json` and fill in your values:

```bash
cp local.settings.json.example local.settings.json
```

Edit `local.settings.json` with your actual credentials:

- **FABRIC_EVENTHUB_CONNECTION_STRING**: Your Azure Event Hub connection string
- **FABRIC_EVENTHUB_NAME**: Your Event Hub name
- **OPENSKY_CLIENT_ID**: Your OpenSky Network username (optional)
- **OPENSKY_CLIENT_SECRET**: Your OpenSky Network password (optional)

### 5. Run locally

```bash
func start
```

## Project Structure

- `function_app.py` - Main Azure Function timer trigger
- `eventhub_connection.py` - Event Hub producer client and data streaming logic
- `opensky_client.py` - OpenSky Network API client
- `country_lookup.py` - Geographic country lookup from coordinates
- `countries.geojson` - GeoJSON data for country boundaries
- `requirements.txt` - Python dependencies

## Deployment

Deploy to Azure Functions using:

```bash
func azure functionapp publish <your-function-app-name>
```

Make sure to configure the application settings in Azure Portal with the same environment variables from `local.settings.json`.

## Data Schema

The function streams flight data with the following structure:

```json
{
  "icao24": "string",
  "callsign": "string",
  "origin_country": "string",
  "current_country": "string",
  "time_position": "integer",
  "last_contact": "integer",
  "longitude": "float",
  "latitude": "float",
  "geo_altitude": "float",
  "on_ground": "boolean",
  "velocity": "float",
  "heading": "float",
  "vertical_rate": "float"
}
```

## License

MIT

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
