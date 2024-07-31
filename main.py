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
    parser.add_argument('--equip', type=int, nargs=2, help='Equip an item (format: slot item)')
    parser.add_argument('--unequip', type=int, help='Unequip an item (format: slot)')
    args = parser.parse_args()

    server = os.getenv('SERVER')
    token = os.getenv('API_TOKEN')
    character = os.getenv('CHARACTER')

    client = ArtifactClient(server, token, character)

    if args.gather:
        GatheringBot(client)
    elif args.attack:
        client.attack_character()
    elif args.move:
        x, y = map(int, args.move.split(','))
        client.move_character(x, y)
    elif args.equip:
        client.equip_item(*args.equip)
    elif args.unequip:
        client.unequip_item(args.unequip)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
