from .connection import Connection

class Player:

    def __init__(self, tableid: int, connection: Connection):
        self.id = id
        self.connection = connection

    def __eq__(self, obj):
        # Who knows if this is what we need right now, but we'll come back to it
        return isinstance(obj, Player) and obj.id == self.id