"""
metadata.py 
-------------------------
Tiny class but writing it anyway 


    Simple wrapper class for reading metadata from a JSON file.
    This keeps the whole pipeline feeling consistent and modular.


"""

import json

class MetadataLoader:
    """
    Just wraps JSON loading so everything
    matches 
    """

    def __init__(self, filepath):
        # Store the path to the JSON file (e.g., "metadata.json")
        self.filepath = filepath

        # Will hold the metadata dictionary once loaded
        self.metadata = {}

    def load(self):
        with open(self.filepath, "r") as f: # Open the metadata JSON file in read mode
            self.metadata = json.load(f) # Parse the JSON file into a Python dictionary
        return self.metadata # Return the parsed metadata so other classes can use it
