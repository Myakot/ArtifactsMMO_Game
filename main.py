import argparse
import os

from icecream import ic
import time
from dotenv import load_dotenv
from client import ArtifactClient

load_dotenv()


class GatheringBot:
    def __init__(self, client):
        self.client = client
        self.cooldown = 25

    def run(self):
        while True:
            self.cooldown = self.client.perform_gathering()
            ic(self.cooldown, 'cooldown')

            # Wait for the cooldown
            time.sleep(self.cooldown)


def main():
    parser = argparse.ArgumentParser(description='Artifact MMO Gathering Bot')
    parser.add_argument('--gather', action='store_true', help='Run auto gathering')
    parser.add_argument('--attack', type=str, help='Attack the tile you are on')
    parser.add_argument('--move', type=str, help='Move to a tile (format: x,y)')
    parser.add_argument('--equip', type=str, help='Equip an item (format: item_code,slot)')
    parser.add_argument('--unequip', type=str, help='Unequip an item (format: slot)')
    parser.add_argument('--deposit', type=str, help='Deposit an item (format: code,quantity)')
    args = parser.parse_args()

    server = os.getenv('SERVER')
    token = os.getenv('API_TOKEN')
    character = os.getenv('CHARACTER')

    client = ArtifactClient(server, token, character)

    if args.gather:
        GatheringBot(client).run()
    elif args.attack:
        client.attack_character()
    elif args.move:
        x, y = map(int, args.move.split(','))
        client.move_character(x, y)
    elif args.equip:
        item_code, slot = map(str, args.equip.split(','))
        client.equip_item(item_code, slot)
    elif args.unequip:
        client.unequip_item(args.unequip)
    elif args.deposit:
        code, quantity = map(str, args.deposit.split(','))
        client.deposit(code, quantity)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
