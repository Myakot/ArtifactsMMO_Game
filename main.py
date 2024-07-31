import os
from icecream import ic
import requests
import time
from dotenv import load_dotenv

load_dotenv()


class ArtifactClient:

    def __init__(self, server, token, character):
        self.server = server
        self.token = token
        self.character = character
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def move_character(self, x, y):
        url = f"{self.server}/my/{self.character}/action/move"
        data = {
            "destination": {
                "x": x,
                "y": y
            }
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def equip_item(self, slot, item_code):
        url = f"{self.server}/my/{self.character}/action/equip"
        data = {
            "slot": slot,
            "item": {
                "code": item_code
            }
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def unequip_item(self, slot):
        url = f"{self.server}/my/{self.character}/action/unequip"
        data = {
            "slot": slot
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def perform_gathering(self):
        url = f"{self.server}/my/{self.character}/action/gathering"
        response = requests.post(url, headers=self.headers)
        ic(response.status_code)
        data = response.json()
        if response.status_code == 200:
            return data['data']['cooldown']['total_seconds']


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


if __name__ == "__main__":
    server = 'https://api.artifactsmmo.com'
    token = os.getenv('API_TOKEN')
    character = "First_Victim"

    client = ArtifactClient(server, token, character)
    bot = GatheringBot(client)
    bot.run()
