import requests
from icecream import ic


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
        ic('Initialized ArtifactClient')

    def move_character(self, x, y):
        ic('Moving character, received x and y are:', x, y)
        url = f"{self.server}/my/{self.character}/action/move"
        data = {
            "x": x,
            "y": y
        }
        response = requests.post(url, headers=self.headers, json=data)
        ic('Moving to {}'.format(x, y), response.status_code)
        return response.json()

    def attack_character(self):
        url = f"{self.server}/my/{self.character}/action/attack"
        response = requests.post(url, headers=self.headers)
        ic(response.status_code)
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
        ic(response.status_code)
        return response.json()

    def unequip_item(self, slot):
        url = f"{self.server}/my/{self.character}/action/unequip"
        data = {
            "slot": slot
        }
        response = requests.post(url, headers=self.headers, json=data)
        ic(response.status_code)
        return response.json()

    def perform_gathering(self):
        url = f"{self.server}/my/{self.character}/action/gathering"
        response = requests.post(url, headers=self.headers)
        ic(response.status_code)
        data = response.json()
        ic(response.status_code)
        return data['data']['cooldown']['total_seconds']