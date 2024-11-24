from fastapi import FastAPI, Request
import logging
from datetime import datetime
import uvicorn
from acc_list import main_wallets, TRACKED_TOKENS
from dotenv import load_dotenv
import requests
import os

load_dotenv(override=True)

logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    handlers=[logging.FileHandler("token_transfers.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
app = FastAPI()

processed_txs = {}


# Add Telegram sending function
def send_telegram_message(message):
    token_tg = os.getenv("TELEGRAM_TOKEN")
    id_tg = os.getenv("TELEGRAM_ID")

    url = f"https://api.telegram.org/bot{token_tg}/sendMessage"
    params = {
        "chat_id": id_tg,
        "text": message,
        "parse_mode": "HTML",
    }

    try:
        response = requests.post(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")


@app.post("/")
async def webhook(request: Request):
    try:
        data = await request.json()

        if isinstance(data, list):
            for event in data:
                await process_event(event)
        else:
            await process_event(data)

        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {"status": "error", "message": str(e)}


async def process_event(event):
    try:
        if not event.get("tokenTransfers"):
            return

        tx_signature = event.get("signature")
        if tx_signature in processed_txs:
            return

        processed_txs[tx_signature] = datetime.now()

        for transfer in event["tokenTransfers"]:
            token_address = transfer.get("mint")

            if token_address not in TRACKED_TOKENS:
                continue

            to_address = transfer.get("toUserAccount")

            # Only process incoming transfers to our wallets
            if to_address not in main_wallets:
                continue

            token_name = TRACKED_TOKENS[token_address]
            from_address = transfer.get("fromUserAccount")
            amount = float(transfer.get("tokenAmount", 0))

            transfer_info = (
                f"\n{'='*50}\n"
                f"NEW {token_name} INCOMING TRANSFER on ROBINHOOD!\n"
                f"Amount: {amount:,.2f}\n"
                f"From: {from_address}\n"
                f"To: {to_address}\n"
                f"Transaction: {tx_signature}\n"
                f"Timestamp: {datetime.now()}\n"
                f"{'='*50}"
            )

            # Log to console/file
            logger.warning(transfer_info)

            # Telegram notification
            message = (
                f"🔔 <b>{token_name} Robinhood transfer</b>\n\n"
                f"Amount: {amount:,.2f}\n"
                f"<a href='https://solscan.io/tx/{tx_signature}'>View Transaction</a>"
            )

            logger.debug("Attempting to send Telegram message...")
            send_telegram_message(message)
            logger.debug("Telegram message sent (or attempted)")

    except Exception as e:
        logger.error(f"Error in process_event: {str(e)}", exc_info=True)


@app.get("/")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    print("Server starting on port 8000...")
    print(f"Monitoring incoming transfers to wallets: {main_wallets}")
    print(f"Tracking tokens: {list(TRACKED_TOKENS.values())}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
