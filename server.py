from fastapi import FastAPI, Request
import logging
from datetime import datetime
import uvicorn
from acc_list import main_wallets, TRACKED_TOKENS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("token_transfers.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
app = FastAPI()

# Cache for deduplication
processed_txs = {}


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
        logger.error(f"Error in webhook endpoint: {e}")
        return {"status": "error", "message": str(e)}


async def process_event(event):
    try:
        # Only process if there are token transfers
        if not event.get("tokenTransfers"):
            return

        tx_signature = event.get("signature")
        if tx_signature in processed_txs:
            return

        processed_txs[tx_signature] = datetime.now()

        for transfer in event["tokenTransfers"]:
            token_address = transfer.get("mint")

            # Only process tracked tokens
            if token_address not in TRACKED_TOKENS:
                continue

            token_name = TRACKED_TOKENS[token_address]
            from_address = transfer.get("fromUserAccount")
            to_address = transfer.get("toUserAccount")

            # Only process if our wallets are involved
            if not any(wallet in [from_address, to_address] for wallet in main_wallets):
                continue

            raw_amount = transfer.get("amount", 0)
            decimals = {"USDC": 6, "BONK": 5, "WIF": 6, "JUP": 6}.get(token_name, 6)

            amount = float(raw_amount) / (10**decimals)
            direction = "INCOMING" if to_address in main_wallets else "OUTGOING"

            transfer_info = (
                f"\n{'='*50}\n"
                f"NEW {direction} TRANSFER DETECTED!\n"
                f"Token: {token_name}\n"
                f"Amount: {amount:,.6f}\n"
                f"From: {from_address}\n"
                f"To: {to_address}\n"
                f"Transaction: {tx_signature}\n"
                f"Timestamp: {datetime.now()}\n"
                f"{'='*50}"
            )

            print(transfer_info)
            logger.info(transfer_info)

    except Exception as e:
        logger.error(f"Error processing event: {e}")


@app.get("/")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    print("Server starting on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
