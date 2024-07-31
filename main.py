import argparse
import os
import time

from icecream import ic
from dotenv import load_dotenv

from client import ArtifactClient

load_dotenv()


class Bot:

    def __init__(self, client, task, args):
        self.client = client
        self.task = task
        self.args = args
        self.cooldown = 25

    def run(self):
        while True:
            if self.task == 'gather':
                self.cooldown = self.client.gathering()
            elif self.task == 'attack':
                self.client.attack()
            elif self.task == 'move':
                x, y = map(int, self.args.move.split(','))
                self.client.move_character(x, y)
                break
            elif self.task == 'equip':
                item_id = self.args.equip
                self.client.equip_item(item_id)
                break
            elif self.task == 'unequip':
                item_id = self.args.unequip
                self.client.unequip_item(item_id)
                break
            elif self.task == 'deposit':
                ic('starting depositing')
                time.sleep(self.cooldown) # in case another action just happened
                self.client.move_character(4, 1) # move to bank
                ic('moved to bank')
                time.sleep(self.cooldown) # wait after moving
                item_id, quantity = map(str, self.args.deposit.split(','))
                self.client.deposit(item_id, quantity)
                break

            ic(self.cooldown, 'cooldown')

            # Wait for the cooldown
            time.sleep(self.cooldown)


def main():
    parser = argparse.ArgumentParser(description='Artifact MMO Bot')
    parser.add_argument('--gather', action='store_true', help='Run auto gathering')
    parser.add_argument('--attack', action='store_true', help='Attack the tile you are on')
    parser.add_argument('--move', nargs='?', help='Move to a tile')
    parser.add_argument('--equip', nargs='?', help='Equip an item')
    parser.add_argument('--unequip', nargs='?', help='Unequip an item')
    parser.add_argument('--deposit', nargs='?', help='Deposit an item')
    args = parser.parse_args()
    server = os.getenv('SERVER')
    token = os.getenv('API_TOKEN')
    character = os.getenv('CHARACTER')
    client = ArtifactClient(server, token, character)

    if args.gather:
        bot = Bot(client, 'gather', args)
        bot.run()
    elif args.attack:
        bot = Bot(client, 'attack', args)
        bot.run()
    elif args.move:
        bot = Bot(client, 'move', args)
        bot.run()
    elif args.equip:
        bot = Bot(client, 'equip', args)
        bot.run()
    elif args.unequip:
        bot = Bot(client, 'unequip', args)
        bot.run()
    elif args.deposit:
        bot = Bot(client, 'deposit', args)
        bot.run()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
