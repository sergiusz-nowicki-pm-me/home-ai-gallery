import os
from src.album_entry import AlbumEntry
from src.json_file import JsonFile


class Album:
    def __init__(self, album_path):
        print(f'Loading album {album_path}')
        metadata_json_file = JsonFile(os.path.join(album_path, '.metadata'))
        entries = (AlbumEntry(os.path.join(album_path, path) , metadata_json_file) for path in os.listdir(album_path) if os.path.isfile(path))
        self.entries = (e for e in entries if not e.is_generic())


    def get_entries(self, search_condition):
        return (e for e in self.entries if e.is_satisfying(search_condition))