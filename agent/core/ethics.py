# agent/core/ethics.py
class EthicsEngine:
    def __init__(self):
        self.rules = open("../config/ethics.txt").read().lower()

    def is_allowed(self, action):
        forbidden = ["attack_civilian", "steal_data", "spy_children"]
        return not any(f in self.rules for f in forbidden)