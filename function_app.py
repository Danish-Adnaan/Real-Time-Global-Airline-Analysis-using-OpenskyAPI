#type: ignore
import logging
import azure.functions as func
from eventhub_connection import send_flight_once

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */4 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
async def FabricIngestTimer(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    await send_flight_once()
    logging.info('Fabric ingestion completed successfully.')
