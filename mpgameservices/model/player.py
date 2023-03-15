from typing import Dict
class Player:

    def __init__(self, id: int, stack: float):
        self.id = id
        self.stack = stack

    def __eq__(self, obj):
        # Who knows if this is what we need right now, but we'll come back to it
        return isinstance(obj, Player) and obj.id == self.id
    
    def serialize(self) -> Dict:
        return {'id': self.id, 'stack': self.stack}