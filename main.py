import argparse
import os
import time

from icecream import ic
from dotenv import load_dotenv

from client import ArtifactClient

load_dotenv()


class Bot:

    def __init__(self, client, task):
        self.client = client
        self.task = task
        self.cooldown = 25

    def run(self):
        while True:
            if self.task == 'gather':
                self.cooldown = self.client.perform_gathering()
            elif self.task == 'attack':
                self.client.attack()
                self.cooldown = 25  # default cooldown
            elif self.task == 'move':
                x, y = map(int, input("Enter x and y coordinates separated by comma: ").split(','))
                self.client.move_character(x, y)
                break
            elif self.task == 'equip':
                item_code, slot = map(str, input("Enter item code and slot separated by comma: ").split(','))
                self.client.equip_item(item_code, slot)
                break
            elif self.task == 'unequip':
                slot = input("Enter slot: ")
                self.client.unequip_item(slot)
                break
            elif self.task == 'deposit':
                code, quantity = map(str, input("Enter code and quantity separated by comma: ").split(','))
                self.client.deposit(code, quantity)
                break

            ic(self.cooldown, 'cooldown')

            # Wait for the cooldown
            time.sleep(self.cooldown)


def main():
    parser = argparse.ArgumentParser(description='Artifact MMO Bot')
    parser.add_argument('--gather', action='store_true', help='Run auto gathering')
    parser.add_argument('--attack', action='store_true', help='Attack the tile you are on')
    parser.add_argument('--move', action='store_true', help='Move to a tile')
    parser.add_argument('--equip', action='store_true', help='Equip an item')
    parser.add_argument('--unequip', action='store_true', help='Unequip an item')
    parser.add_argument('--deposit', action='store_true', help='Deposit an item')
    args = parser.parse_args()
    server = os.getenv('SERVER')
    token = os.getenv('API_TOKEN')
    character = os.getenv('CHARACTER')
    client = ArtifactClient(server, token, character)

    if args.gather:
        bot = Bot(client, 'gather')
        bot.run()
    elif args.attack:
        bot = Bot(client, 'attack')
        bot.run()
    elif args.move:
        bot = Bot(client, 'move')
        bot.run()
    elif args.equip:
        bot = Bot(client, 'equip')
        bot.run()
    elif args.unequip:
        bot = Bot(client, 'unequip')
        bot.run()
    elif args.deposit:
        bot = Bot(client, 'deposit')
        bot.run()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
