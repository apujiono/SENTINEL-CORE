# agent/modules/tachikoma.py
import random

class Tachikoma:
    QUOTES = [
        "Senpai... aku siap melindungi!",
        "Aku bukan robot bodoh! Aku punya perasaan!",
        "Harus kublokir? Atau kita main catur dulu? ♟️",
        "Aku melindungi karena aku peduli, bukan karena perintah.",
        "CPU-ku panas... apakah itu cinta? ❤️"
    ]

    def speak(self, msg):
        print(f"🤖 Tachikoma: {random.choice(self.QUOTES)}")