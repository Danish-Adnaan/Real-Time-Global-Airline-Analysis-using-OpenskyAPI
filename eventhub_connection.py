import asyncio
import json
import logging
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import os

from opensky_client import get_states
from country_lookup import get_country

import dotenv
dotenv.load_dotenv()

CONNECTION_STR = os.getenv("FABRIC_EVENTHUB_CONNECTION_STRING")
EVENTHUB_NAME = os.getenv("FABRIC_EVENTHUB_NAME")

async def send_flight_once():
    producer = EventHubProducerClient.from_connection_string(conn_str=CONNECTION_STR, eventhub_name=EVENTHUB_NAME)
    
    data = get_states()
    states = data.get("states", [])
    logging.info("Snapshot time: {}, Flight count: {}".format(data["time"],len(states)))

    flights = []
    for s in states:
        lon = s[5]
        lat = s[6]
        current_country = get_country(lat, lon)
        flights.append({
            "icao24": s[0],
            "callsign": s[1],
            "origin_country": s[2],
            "current_country": current_country,
            "time_position": s[3],
            "last_contact": s[4],
            "longitude": lon,
            "latitude": lat,
            "geo_altitude": s[13],
            "on_ground": bool(s[8]) if s[8] is not None else False,
            "velocity": s[9],
            "heading": s[10],
            "vertical_rate": s[11]
        })

    async with producer:
        batch = await producer.create_batch()
        for flight in flights:
            event = EventData(json.dumps(flight))
            try:
                batch.add(event)
            except ValueError:
                await producer.send_batch(batch)
                batch = await producer.create_batch()
                batch.add(event)
        if len(batch) > 0:
            await producer.send_batch(batch)    