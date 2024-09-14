import requests

from smart_airdrop_claimer import base
from core.headers import headers


def get_info(data, proxies=None):
    url = "https://api.hamsterkombatgame.io/clicker/sync"

    try:
        response = requests.post(
            url=url,
            headers=headers(data=data),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        total_coins = round(data["clickerUser"]["totalCoins"], 0)
        balance_coins = round(data["clickerUser"]["balanceCoins"], 0)
        available_taps = data["clickerUser"]["availableTaps"]

        base.log(
            f"{base.green}Total Coins: {base.white}{total_coins:,} - {base.green}Balance Coins: {base.white}{balance_coins:,}"
        )

        return available_taps, balance_coins
    except:
        return None
