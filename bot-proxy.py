import sys

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core.info import get_info
from core.tapper import process_tap
from core.upgrade import process_buy_card

import time
import random
import json


class HamsterKombat:
    def __init__(self):
        # Get file directory
        self.data_file = base.file_path(file_name="data-proxy.json")
        self.config_file = base.file_path(file_name="config.json")

        # Initialize line
        self.line = base.create_line(length=50)

        # Initialize banner
        self.banner = base.create_banner(game_name="Hamster Kombat")

        # Get config
        self.auto_tap = base.get_config(
            config_file=self.config_file, config_name="auto-tap"
        )

        self.auto_buy_card = base.get_config(
            config_file=self.config_file, config_name="auto-buy-card"
        )

    def main(self):
        while True:
            base.clear_terminal()
            print(self.banner)
            accounts = json.load(open(self.data_file, "r"))["accounts"]
            num_acc = len(accounts)
            base.log(self.line)
            base.log(f"{base.green}Number of accounts: {base.white}{num_acc}")

            for no, account in enumerate(accounts):
                base.log(self.line)
                base.log(f"{base.green}Account number: {base.white}{no+1}/{num_acc}")
                data = account["acc_info"]
                proxy_info = account["proxy_info"]
                parsed_proxy_info = base.parse_proxy_info(proxy_info)
                if parsed_proxy_info is None:
                    break

                actual_ip = base.check_ip(proxy_info=proxy_info)

                proxies = base.format_proxy(proxy_info=proxy_info)

                try:
                    get_info(data=data, proxies=proxies)

                    # Tap
                    if self.auto_tap:
                        base.log(f"{base.yellow}Auto Tap: {base.green}ON")
                        process_tap(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Tap: {base.red}OFF")

                    # Buy card
                    if self.auto_buy_card:
                        base.log(f"{base.yellow}Auto Buy Card: {base.green}ON")
                        process_buy_card(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Buy Card: {base.red}OFF")

                except Exception as e:
                    base.log(f"{base.red}Error: {base.white}{e}")

            print()
            wait_time = random.randint(5, 20)
            base.log(f"{base.yellow}Wait for {wait_time} seconds!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        hamster = HamsterKombat()
        hamster.main()
    except KeyboardInterrupt:
        sys.exit()
