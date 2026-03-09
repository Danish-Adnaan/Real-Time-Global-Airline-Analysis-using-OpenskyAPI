# Azure Flight Data Ingestion

This Azure Function ingests real-time flight data from OpenSky Network API and streams it to an Azure Event Hub for processing in Microsoft Fabric.


<img width="1129" height="638" alt="image" src="https://github.com/user-attachments/assets/8ed4b2d1-a0a9-4295-ab1f-c93af2d6fd95" />


<img width="1131" height="645" alt="image" src="https://github.com/user-attachments/assets/f7f91e5a-6c46-4420-9ff1-e908e4ca211e" />


## 🏗️ Architecture Overview

```mermaid
flowchart LR
    A[OpenSky Network API<br/>Live aircraft states<br/>~4 min cadence] --> B[Python Ingestion<br/>opensky_client.py<br/>eventhub_connection.py]
    
    J[Azure Function App<br/>Timer trigger<br/>Every 4 minutes] --> B
    
    B --> C[Fabric Eventstream<br/>Ingest endpoint]
    C --> D[AirlineDestinationEventhouse<br/>Kusto database]
    
    D --> E1[v_Flights_Current<br/>Materialized View]
    D --> E2[v_Flights_Current_Enriched<br/>Freshness filtering]
    D --> E3[v_Country_Traffic_Snapshot]
    D --> E4[v_Airline_Traffic_Snapshot]
    
    E1 --> F[Power BI Semantic Model<br/>DirectQuery + Dimensions]
    F --> G[Power BI Desktop<br/>DAX measures<br/>2 dashboard pages]
    G --> H[Power BI Service<br/>Live demo]
    
    H --> I[Viewers]

    classDef api fill:#1f77b4,stroke:#4a90e2,color:#fff
    classDef python fill:#ff7f0e,stroke:#ffbb78,color:#fff
    classDef azure fill:#9467bd,stroke:#c492e2,color:#fff
    classDef fabric fill:#2ca02c,stroke:#7de27d,color:#fff
    classDef kql fill:#d62728,stroke:#ff9898,color:#fff
    classDef powerbi fill:#e377c2,stroke:#f7b6d2,color:#fff
    
    class A api
    class B,J python,azure
    class C,D fabric
    class E1,E2,E3,E4 kql
    class F,G,H powerbi
    class I powerbi




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
