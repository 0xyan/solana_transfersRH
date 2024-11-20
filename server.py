from fastapi import FastAPI, Request
import logging
from datetime import datetime
import uvicorn
from acc_list import main_wallets, TRACKED_TOKENS
import requests
import os

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
    try:
        telegram_token = os.getenv("TELEGRAM_TOKEN")
        telegram_id = os.getenv("TELEGRAM_ID")
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"

        payload = {
            "chat_id": telegram_id,
            "text": message,
            "parse_mode": "HTML",  # This allows for basic formatting
        }

        response = requests.post(url, json=payload)
        if response.status_code != 200:
            logger.error(f"Failed to send Telegram message: {response.text}")
    except Exception as e:
        logger.error(f"Error sending Telegram message: {e}")


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
                f"NEW INCOMING TRANSFER!\n"
                f"Token: {token_name}\n"
                f"Amount: {amount:,.6f}\n"
                f"From: {from_address}\n"
                f"To: {to_address}\n"
                f"Transaction: {tx_signature}\n"
                f"Timestamp: {datetime.now()}\n"
                f"{'='*50}"
            )

            # Log to console/file
            logger.warning(transfer_info)

            # Send Telegram notification
            telegram_message = (
                f"🔔 <b>New Incoming Transfer</b>\n\n"
                f"💰 Token: {token_name}\n"
                f"📊 Amount: {amount:,.6f}\n"
                f"📤 From: <code>{from_address[:8]}...{from_address[-8:]}</code>\n"
                f"📥 To: <code>{to_address[:8]}...{to_address[-8:]}</code>\n"
                f"🔗 <a href='https://solscan.io/tx/{tx_signature}'>View Transaction</a>"
            )
            send_telegram_message(telegram_message)

    except Exception as e:
        logger.error(f"Error processing transfer: {str(e)}")


@app.get("/")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    print("Server starting on port 8000...")
    print(f"Monitoring incoming transfers to wallets: {main_wallets}")
    print(f"Tracking tokens: {list(TRACKED_TOKENS.values())}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
