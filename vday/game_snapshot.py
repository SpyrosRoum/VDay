"""
A class that you can use to save and load the game
It holds info about the current game state and options
"""
from dataclasses import dataclass
from datetime import datetime
import pickle
from pathlib import Path

@dataclass
class GameSnapshot:
    """
    Each day has a range of enemies and strength
    so it's not needed to save that info

    The dungeon is also different per day and we save at the start of each day
    so no need to save the dungeon

    Player health is full at the start of each day
    """
    player_max_health: int

    current_day: int

    volume: int

    def save(self):
        """
        Save this object in a file to be  loaded later
        """
        Path("./saves").mkdir(exist_ok=True)

        now = datetime.now()
        fp = f"saves/save_{now.day}_{now.month}_{now.hour}_{now.minute}_{now.second}"
        with open(fp, "wb") as file:
            pickle.dump(self, file)

        print("Saved!")
