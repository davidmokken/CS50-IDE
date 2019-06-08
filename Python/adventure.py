from room import Room
from item import Item
from inventory import Inventory
import sys


class Adventure():
    """
    This is your Adventure game class. It should contains
    necessary attributes and methods to setup and play
    Crowther's text based RPG Adventure.
    """

    def __init__(self, game):
        """
        Create rooms and items for the appropriate 'game' version.
        """
        self.rooms = self.load_rooms(f"data/{game}Rooms.txt")
        self.current_room = self.rooms[1]
        self.items = self.load_items(f"data/{game}Items.txt")
        self.inventory = Inventory()

    def load_rooms(self, filename):
        """
        Load rooms from filename.
        Returns a dictionary of 'id' : Room objects.
        """
        # First we parse all the data we need to create the rooms with.
        # All parsed lines of data are saved to rooms_data.
        rooms_data = []
        with open(filename, "r") as f:
            room_data = []
            for line in f:
                # When there is no blank newline it means there's still data.
                if not line == "\n":
                    room_data.append(line.strip())
                # A blank newline signals all data of a single room is parsed.
                else:
                    rooms_data.append(room_data)
                    room_data = []
        # Append a final time, because the files do not end on a blank newline.
        rooms_data.append(room_data)

        # Create room objects for each set of data we just parsed.
        rooms = {}
        for room_data in rooms_data:
            id = int(room_data[0])
            name = room_data[1]
            description = room_data[2]

            # Initialize a room object and put it in a dictionary with its
            # id as key.
            room = Room(id, name, description)
            rooms[id] = room

        # Add routes to each room we've created with the data from each set
        # we have parsed earlier.
        for room_data in rooms_data:
            id = int(room_data[0])
            # We split to connections into a direction and a room_id.
            connections = room_data[4:]
            connections = [connection.split() for connection in connections]
            # Here we get the current room object that we'll add routes to.
            room = rooms[id]
            # Add routes to a room
            for connection, target_room_id in connections:
                room.add_route(connection, target_room_id)
        return rooms

    def load_items(self, filename):
        """
        Load items from filename
        """
        # First we parse all the data we need to create the items with.
        # All parsed lines of data are saved to items_data.
        items_data = []
        with open(filename, "r") as f:
            item_data = []
            for line in f:
                # When there is no blank newline it means there's still data.
                if not line == "\n":
                    item_data.append(line.strip())
                # A blank newline signals all data of a single room is parsed.
                else:
                    items_data.append(item_data)
                    item_data = []
        # Append a final time, because the files do not end on a blank newline.
        items_data.append(item_data)

        # Create item objects for each set of data we just parsed.
        items = {}
        for item_data in items_data:
            name = item_data[0]
            description = item_data[1]
            initial_room_id = int(item_data[2])

            # Initialize a item object and put it in a dictionary with its
            # initial_room_id as key.
            item = Item(name, description, initial_room_id)
            items[initial_room_id] = initial_room_id

            # Add items to the inventory of a room
            self.rooms[initial_room_id].inventory.add_item(item)

    def game_over(self):
        """
        Check if the game is over.
        Returns a boolean.
        """
        if self.current_room.is_connected("FORCED"):
            return True
        else:
            return False

    def move(self, direction):
        """
        Moves to a different room in the specified direction.
        """
        if direction in self.current_room.conditional_routes and \
                self.current_room.conditional_routes[direction][1] in self.inventory.items:
            next_room = int(self.current_room.conditional_routes[direction][0])
            self.current_room = self.rooms[next_room]
            self.forced_move()
        else:
            next_room = int(self.current_room.routes[direction])
            self.current_room = self.rooms[next_room]
            self.forced_move()

    def play(self):
        """
        Play an Adventure game
        """
        print(f"Welcome, to the Adventure games.\n"
              "May the randomly generated numbers be ever in your favour.\n")

        print(self.current_room)
        description_shown = set()
        description_shown.add(self.rooms[1])

        # Prompt the user for commands until they've won the game.
        while not self.game_over():
            command = (input("> ")).upper()

            # Additional Commands
            if command == 'HELP':
                self.command_help()
            elif command == 'QUIT':
                self.command_quit()
            elif command == 'LOOK':
                self.command_look()
            elif command == 'INVENTORY':
                self.command_inventory()

            # Check if the command is a movement or not.
            elif self.current_room.is_connected(command):
                # TODO: Perform a move.
                self.move(command)
                if self.current_room in description_shown:
                    print(self.current_room.name)
                else:
                    print(self.current_room)
                    description_shown.add(self.current_room)

                if len(self.current_room.inventory.items) != 0:
                    print(self.current_room.inventory)

            elif len(command.split()) == 2:
                command = command.split()
                name_item = command[1]
                if command[0] == 'TAKE':
                    self.take(name_item)
                elif command[0] == 'DROP':
                    self.drop(name_item)
            else:
                print("Invalid command")

        exit(0)

    def forced_move(self):
        """
        Forces a move
        """
        while 'FORCED' in (self.current_room.conditional_routes.keys() or self.current_room.routes.keys()):
            print(self.current_room.description)

            if 'FORCED' in self.current_room.conditional_routes:
                forced = self.current_room.conditional_routes['FORCED'][0]
                forced_condition = self.current_room.conditional_routes['FORCED'][1]
                if forced_condition in self.inventory.items:
                    next_room = int(forced)
                    self.current_room = self.rooms[next_room]
                else:
                    next_room = int(self.current_room.routes['FORCED'])
                    self.current_room = self.rooms[next_room]

            else:
                next_room = int(self.current_room.routes['FORCED'])
                if next_room != 0:
                    self.current_room = self.rooms[next_room]
                else:
                    exit()

    def take(self, name_item):
        """
        Takes an item
        """
        found = False
        for item in list(self.current_room.inventory.items):
            if item == name_item:
                self.inventory.add_item(self.current_room.inventory.items[name_item])
                self.current_room.inventory.remove_item(self.current_room.inventory.items[name_item])
                print(f"{name_item} taken.")
                found = True
        if not found:
            print("No such item.")

    def drop(self, name_item):
        """
        Drops an item
        """
        dropped = False
        for item in list(self.inventory.items):
            # for item in self.inventory.items.keys():
            if item == name_item:
                self.current_room.inventory.add_item(self.inventory.items[name_item])
                self.inventory.remove_item(self.inventory.items[name_item])
                print(f"{name_item} dropped.")
                dropped = True
        if not dropped:
            print("No such item.")

    def command_help(self):
        """
        Help Command
        """
        print("You can move by typing directions such as EAST/WEST/IN/OUT")
        print("QUIT quits the game.")
        print("HELP prints instructions for the game.")
        print("INVENTORY lists the item in your inventory.")
        print("LOOK lists the complete description of the room and its contents.")
        print("TAKE <item> take item from the room.")
        print("DROP <item> drop item from your inventory.")

    def command_quit(self):
        """
        Quit Command
        """
        print("Thanks for playing!")
        exit()

    def command_look(self):
        """
        Look Command
        """
        print(self.current_room)
        if len(self.current_room.inventory.items) != 0:
            print(self.current_room.inventory)
        else:
            print("Room is empty")

    def command_inventory(self):
        """
        Shows player inventory
        """
        if len(self.inventory.items) != 0:
            print(self.inventory)
        else:
            print("Your inventory is empty.")


if __name__ == "__main__":

    if ((len(sys.argv) != 2) or (sys.argv[1].isalpha == False)):
        print("Error. Choose a game mode")
        exit(1)

    game = sys.argv[1]

    if game not in ("Tiny", "Small", "Crowther"):
        print("Choose correct game mode")
        exit(1)
    adventure = Adventure(game)

    adventure.play()

