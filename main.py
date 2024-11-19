import requests
import os
from dotenv import load_dotenv
from acc_list import main_wallets
import json

load_dotenv()
API_KEY = os.getenv("HELIUS_API_KEY")
WEBHOOK_URL = "https://41d3-171-96-191-176.ngrok-free.app"


def get_existing_webhooks():
    url = f"https://api.helius.xyz/v0/webhooks?api-key={API_KEY}"
    response = requests.get(url)
    webhooks = response.json()
    print(
        f"\nFound {len(webhooks)} existing webhooks: "
        + ", ".join([hook["webhookID"] for hook in webhooks])
    )
    return webhooks


def delete_webhook(webhook_id):
    url = f"https://api.helius.xyz/v0/webhooks/{webhook_id}?api-key={API_KEY}"
    response = requests.delete(url)
    print(f"Deleted webhook {webhook_id}: {response.status_code}")


def register_webhooks(accounts):
    # Delete existing webhooks
    existing = get_existing_webhooks()
    for webhook in existing:
        delete_webhook(webhook["webhookID"])

    # Create single webhook for all accounts
    url = f"https://api.helius.xyz/v0/webhooks?api-key={API_KEY}"
    payload = {
        "webhookURL": WEBHOOK_URL,
        "transactionTypes": ["TRANSFER"],
        "accountAddresses": accounts,  # All 9,460 accounts in one webhook
        "webhookType": "enhanced",
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"Successfully registered webhook for {len(accounts)} accounts")
        return True, response.json()
    return False, None


if __name__ == "__main__":
    print("Starting webhook registration...")
    print(
        f"Using API key: {API_KEY[:4]}...{API_KEY[-4:]}"
    )  # Show first/last 4 chars of API key
    print(f"Webhook URL: {WEBHOOK_URL}")
    print(f"Monitoring wallets: {len(main_wallets)}")

    status, response = register_webhooks(main_wallets)

    if status:
        print("\nWebhook registration successful!")
    else:
        print("\nWebhook registration failed!")
