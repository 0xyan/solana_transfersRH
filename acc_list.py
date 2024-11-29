import pandas as pd

MAIN_WALLETS = [
    "AeBwztwXScyNNuQCEdhS54wttRQrw3Nj1UtqddzB4C7b",  # Solana dep wallet + USDC from Circle treasury
    "8Tp9fFkZ2KcRBLYDTUNXo98Ez6ojGb6MZEPXfGDdeBzG",  # Cold (only interacts with MM receiver)
    "6brjeZNfSpqjWoo16z1YbywKguAruXZhNz9bJMVZE8pD",  # MM receiver
    "CdkLi5GK8kGTNmHCTe1dem2dXxgU2V2Yxh5s4xPuk9UY",  # USDC hot wallet
    "AbdxrST5risqoSDB76Yk6cvGJRdrHrGXxUrZ4VxZHGZU",  # WIF hot wallet
    "CQWxRn2iW5qSxfBaEDaZSym4ZhVjpeXsgSDvw9PehnLj",  # WIF BONK testing wallet
]

EXCLUDED_WALLETS = {
    "BY4StcU9Y2BpgH8quZzorg31EGE4L1rjomN8FNsCBEcx",  # htx hot wallet
    "5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9",  # binance 2
    "FWznbcNXWQuHTawe9RxvQ2LdCENssh12dsznf4RiouN5",  # kraken
    "9un5wqE3q4oCjyrDkwsdD48KteCJitQX5978Vh7KKxHo",  # OKX 2
    "5sTQ5ih7xtctBhMXHr3f1aWdaXazWrWfoehqWdqWnTFP",  # wintermute
    "5BCgqYg51CANe8qUMPYWJsqRA4Y8HnyfmvkoJxcEmQfY",  # bybit
    "AobVSwdW9BbpMdJvTqeCN4hPAmh4rHm7vwLnQ5ATSyrS",  # cryptcom 2
    "H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS",  # cb 1
    "2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm",  # cb 2
}

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
    "ukHH6c7mMyiWCf1b9pnWe25TSpkDDt3H5pQZgZ74J82": "BOME",
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

        # Remove excluded wallets
        all_wallets = [w for w in all_wallets if w not in EXCLUDED_WALLETS]

        print(f"Loaded unique wallets: {len(all_wallets)}")
        return all_wallets
    except Exception as e:
        print(f"Error loading wallets: {e}")
        return [
            w for w in MAIN_WALLETS if w not in EXCLUDED_WALLETS
        ]  # Also filter fallback list


main_wallets = load_all_wallets()
