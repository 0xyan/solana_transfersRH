import requests
import os
from dotenv import load_dotenv
from acc_list import main_wallets
import json

load_dotenv()
API_KEY = os.getenv("HELIUS_API_KEY")
WEBHOOK_URL = "https://ec7a-171-97-216-9.ngrok-free.app"


def get_existing_webhooks():
    url = f"https://api.helius.xyz/v0/webhooks?api-key={API_KEY}"
    response = requests.get(url)
    print(f"\nExisting webhooks: {response.json()}")
    return response.json()


def delete_webhook(webhook_id):
    url = f"https://api.helius.xyz/v0/webhooks/{webhook_id}?api-key={API_KEY}"
    response = requests.delete(url)
    print(f"Deleted webhook {webhook_id}: {response.status_code}")


def register_webhooks(accounts):
    # Delete existing webhooks
    existing = get_existing_webhooks()
    for webhook in existing:
        delete_webhook(webhook["webhookID"])

    # Register new webhook
    url = f"https://api.helius.xyz/v0/webhooks?api-key={API_KEY}"
    payload = {
        "webhookURL": WEBHOOK_URL,
        "transactionTypes": ["TRANSFER"],
        "accountAddresses": accounts,
        "webhookType": "enhanced",
    }

    print(f"\nSending payload: {payload}")

    try:
        response = requests.post(url, json=payload)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")

        if response.status_code != 200:
            print(f"Error details: {response.text}")

        return response.status_code, (
            response.json() if response.status_code == 200 else None
        )

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return 500, None
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return 500, None


if __name__ == "__main__":
    print("Starting webhook registration...")
    print(
        f"Using API key: {API_KEY[:4]}...{API_KEY[-4:]}"
    )  # Show first/last 4 chars of API key
    print(f"Webhook URL: {WEBHOOK_URL}")
    print(f"Monitoring wallets: {main_wallets}")

    status, response = register_webhooks(main_wallets)

    if status == 200:
        print("\nWebhook registration successful!")
    else:
        print("\nWebhook registration failed!")
