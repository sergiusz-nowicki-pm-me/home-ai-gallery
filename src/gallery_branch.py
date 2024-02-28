import os

from src.album import Album


class GalleryBranch:
    def __init__(self, base_path):
        self.base_path = base_path
        self.albums = []
        self.__load_albums(self.base_path)
        
        
    def __load_albums(self, path):
        is_album = False
        for new_path in os.path.listdir(self.base_path):
            if os.path.isdir(new_path):
                self.__load_albums(new_path)
            else:
                is_album = True
        if is_album:
            self.albums.append(Album(path))
        
        
    def get_entries(self, search_condition):
        result = []
        for album in self.albums:
            result.extend(album.get_entries(search_condition))
        return result