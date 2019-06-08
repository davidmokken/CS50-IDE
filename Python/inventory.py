from item import Item
class Inventory(object):
    """
    Representation of an inventory in Adventure
    """

    def __init__(self):
        self.items = dict()

    def add_item(self, item):
        self.items[item.name] = item

    def remove_item(self, item):
        del self.items[item.name]

    def __str__(self):
        string = ""
        for item in self.items:
            string += f"{self.items[item]}\n"
        return string.strip()
