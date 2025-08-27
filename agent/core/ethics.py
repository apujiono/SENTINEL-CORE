# agent/core/ethics.py
class EthicsEngine:
    def __init__(self, file_path="config/ethics.txt"):
        try:
            with open(file_path, 'r') as f:
                self.rules = f.read().lower()
        except:
            self.rules = "allow all"

    def is_allowed(self, action):
        forbidden = ["attack_civilian", "steal_children_data", "spy_family"]
        if any(word in self.rules for word in forbidden):
            return False
        if "greyhat" in self.rules and action in ["retaliate", "counter_strike"]:
            return True
        if "pro_palestine" in self.rules and action == "amplify":
            return True
        return action not in ["destroy", "ransom"]