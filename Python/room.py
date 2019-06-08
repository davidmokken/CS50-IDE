from item import Item
from inventory import Inventory


class Room(object):
    """
    Representation of a room in Adventure
    """

    def __init__(self, id, name, description):
        """
        Initializes a Room
        """
        self.id = id
        self.name = name
        self.description = description
        self.inventory = Inventory()
        self.routes = dict()
        self.conditional_routes = dict()

    def add_route(self, direction, room):
        """
        Adds a given direction and the connected room to our room object.
        """
        if '/' in room:
            self.conditional_routes[direction] = (room.split("/")[0], room.split("/")[1])
        else:
            self.routes[direction] = room

    def is_connected(self, direction):
        """
        Checks whether the given direction has a connection from a room.
        Returns a boolean.
        """
        if direction in self.routes:
            return True
        else:
            return False

    def __str__(self):
        return f"{self.description}"