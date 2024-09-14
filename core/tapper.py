import requests
import datetime

from smart_airdrop_claimer import base
from core.headers import headers
from core.info import get_info


def tap(data, tap_count, proxies=None):
    url = "https://api.hamsterkombatgame.io/clicker/tap"
    current_time = datetime.datetime.now()
    current_timestamp = int(current_time.timestamp())
    payload = {"count": tap_count, "availableTaps": 5, "timestamp": current_timestamp}

    try:
        response = requests.post(
            url=url,
            headers=headers(data=data),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        return data
    except:
        return None


def buy_boost(data, proxies=None):
    url = "https://api.hamsterkombatgame.io/clicker/buy-boost"
    current_time = datetime.datetime.now()
    current_timestamp = int(current_time.timestamp())
    payload = {"boostId": "BoostFullAvailableTaps", "timestamp": current_timestamp}

    try:
        response = requests.post(
            url=url,
            headers=headers(data=data),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        return data
    except:
        return None


def process_tap(data, proxies=None):
    while True:
        available_taps, balance_coins = get_info(data=data, proxies=proxies)

        if available_taps is not None:
            if available_taps > 50:
                start_tap = tap(data=data, tap_count=available_taps, proxies=proxies)
                if start_tap:
                    total_coins = round(start_tap["clickerUser"]["totalCoins"], 0)
                    balance_coins = round(start_tap["clickerUser"]["balanceCoins"], 0)
                    available_taps = start_tap["clickerUser"]["availableTaps"]
                    base.log(
                        f"{base.white}Auto Tap: {base.green}Success | Total Coins: {base.white}{total_coins:,} - {base.green}Balance Coins: {base.white}{balance_coins:,} - {base.green}Available Taps: {base.white}{available_taps}"
                    )
                else:
                    base.log(f"{base.white}Auto Tap: {base.red}Fail")
                    break
            else:
                base.log(
                    f"{base.white}Auto Tap: {base.red}Energy too low to tap, checking boost"
                )
                start_buy_boost = buy_boost(data=data, proxies=proxies)
                try:
                    boosts = start_buy_boost["clickerUser"]["boosts"]
                    base.log(f"{base.white}Auto Tap: {base.green}Buy boost success")
                except:
                    error_message = start_buy_boost["error_message"]
                    base.log(f"{base.white}Auto Tap: {base.red}{error_message}")
                    break
        else:
            base.log(f"{base.white}Auto Tap: {base.red}Get available taps fail")
            break
