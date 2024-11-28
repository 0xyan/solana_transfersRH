import pandas as pd

MAIN_WALLETS = [
    "AeBwztwXScyNNuQCEdhS54wttRQrw3Nj1UtqddzB4C7b",  # Solana dep wallet + USDC from Circle treasury
    "8Tp9fFkZ2KcRBLYDTUNXo98Ez6ojGb6MZEPXfGDdeBzG",  # Cold (only interacts with MM receiver)
    "6brjeZNfSpqjWoo16z1YbywKguAruXZhNz9bJMVZE8pD",  # MM receiver
    "CdkLi5GK8kGTNmHCTe1dem2dXxgU2V2Yxh5s4xPuk9UY",  # USDC hot wallet
    "AbdxrST5risqoSDB76Yk6cvGJRdrHrGXxUrZ4VxZHGZU",  # WIF hot wallet
    "CQWxRn2iW5qSxfBaEDaZSym4ZhVjpeXsgSDvw9PehnLj",  # WIF BONK testing wallet
]

TRACKED_TOKENS = {
    "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263": "BONK",
    "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R": "RAY",
    "HZ1JovNiVvGrGNiiYvEozEVgZ58xaU3RKwX8eACQBCt3": "PYTH",
    "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN": "JUP",
    "85VBFQZC9TZkfaptBWjvUw7YbZjy52A6mjtPGjstQAmQ": "W",
    "Grass7B4RdKfBCjTKgSqnXkqjwiGvQyFbuSCUJr3XXjs": "GRASS",
    "METAewgxyPbgwsseH8T16a39CQ5VyVxZi9zXiDPY18m": "MPLX",
    "KMNo3nJsBXfcpJTVhZcXLW7RmTwTt4GVFE7suUBo9sS": "KMNO",
    "7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr": "POPCAT",
    "2qEHjDLDLbuBgRYvsxhc5D6uDWAivNFZGan56P1tpump": "PNUT",
    "CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump": "GOAT",
    "MEW1gQWJ3nEXg2qgERiKu7FAFj79PHvQVREQUzScPP5": "MEW",
    "85VBFQZC9TZkfaptBWjvUw7YbZjy52A6mjtPGjstQAmQ": "BOME",
    "A8C3xuqscfmyLrte3VmTqrAq8kgMASius9AFNANwpump": "FWOG",
    "8x5VqbHA8D7NkD52uNuS5nnt3PwA8pLD34ymskeSo2Wn": "ZEREBRO",
    "GJAFwWjJ3vnTsrQVabjBVK2TYB1YtRCQXRDfDgUnpump": "ACT",
    "ED5nyyWEzpPPiWimP8vYm7sD7TD3LAt3Q3gRTWHzPJBY": "MOODENG",
    "63LfDmNb3MQ8mw9MtZ2To9bEA2M71kZUUGq5tiJxcqj9": "GIGA",
    "Df6yfrKC8kZE3KNkrHERKzAetSxbrWeniQfyJY4Jpump": "CHILLGUY",
    "9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump": "FARTCOIN",
    "WENWENvqqNya429ubCdR81ZmD69brwQaaBYY6p3LCpk": "WEN",
}


def load_all_wallets(csv_path="deposit_wallets.csv"):
    try:
        # Load deposit wallets from CSV
        df = pd.read_csv(csv_path)
        wallet_column = df.columns[0]
        deposit_wallets = df[wallet_column].unique().tolist()

        # Combine with main wallets and remove any duplicates
        all_wallets = list(set(MAIN_WALLETS + deposit_wallets))

        print(f"Loaded unique wallets: {len(all_wallets)}")

        return all_wallets
    except Exception as e:
        print(f"Error loading wallets: {e}")
        return MAIN_WALLETS  # Fallback to main wallets if CSV loading fails


# Don't load wallets immediately, create a function to get them
def get_main_wallets():
    return load_all_wallets()
