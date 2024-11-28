import requests
from time import sleep
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
from dotenv import load_dotenv
from acc_list import get_main_wallets

load_dotenv(override=True)

API_KEY = os.getenv("HELIUS_API_KEY")
WEBHOOK_URL = "https://54.79.31.7:80"


def create_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def get_existing_webhooks():
    url = f"https://api.helius.xyz/v0/webhooks?api-key={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        webhooks = response.json()

        if webhooks:
            active_webhooks = [w for w in webhooks if w.get("active", False)]
            print(f"\nFound {len(active_webhooks)} active webhooks")
            return webhooks
        return []
    except Exception as e:
        print(f"Warning: Could not fetch existing webhooks: {e}")
        print("Continuing with webhook registration anyway...")
        return []


def register_webhooks(accounts):
    _ = get_existing_webhooks()

    url = f"https://api.helius.xyz/v0/webhooks?api-key={API_KEY}"
    payload = {
        "webhookURL": WEBHOOK_URL,
        "transactionTypes": ["TRANSFER"],
        "accountAddresses": accounts,
        "webhookType": "enhanced",
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        webhook_id = response.json().get("webhookID", "N/A")
        print(f"Successfully registered new webhook (ID: {webhook_id})")
        return True, {"webhookID": webhook_id}
    except Exception as e:
        print(f"Failed to create webhook: {e}")
        return False, None


if __name__ == "__main__":
    print("Starting webhook registration...")
    print(f"Using API key: {API_KEY[:4]}...{API_KEY[-4:]}")
    print(f"Webhook URL: {WEBHOOK_URL}")

    main_wallets = get_main_wallets()
    print(f"Number of wallets to monitor: {len(main_wallets)}")

    status, response = register_webhooks(main_wallets)

    if status:
        print("\nWebhook registration successful!")
        print("Webhook ID:", response.get("webhookID", "N/A"))
    else:
        print("\nWebhook registration failed!")
