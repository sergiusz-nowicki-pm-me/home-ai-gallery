import os
from src.album_entry import AlbumEntry
from src.json_file import JsonFile


class Album:
    def __init__(self, album_path):
        print(f'Loading album {album_path}')
        metadata_json_file = JsonFile(os.path.join(album_path, '.metadata'))
        entries = []
        for name in os.listdir(album_path):
            if name != '.metadata':
                entry_path = os.path.join(album_path, name)
                if os.path.isfile(entry_path):
                    entries.append(AlbumEntry(entry_path, metadata_json_file))
        self.entries = [e for e in entries if not e.is_generic()]


    def get_entries(self, search_condition):
        return (e for e in self.entries if e.is_satisfying(search_condition))