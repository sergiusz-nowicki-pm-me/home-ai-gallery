import os
from src.album_entry import AlbumEntry
from src.json_file import JsonFile


class Album:
    def __init__(self, album_path):
        self.metadata_json_file = JsonFile(album_path)


    def get_entries(self, search_condition):
        entries = (AlbumEntry(path) for path in os.listdir(self.album_path) if os.path.isfile(path))
        # filter out non image entries
        return (e for e in entries if not e.is_generic())