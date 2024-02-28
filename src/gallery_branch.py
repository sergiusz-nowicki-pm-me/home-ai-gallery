import os

from src.album import Album


class GalleryBranch:
    def __init__(self, base_path):
        print(f'Loading branch {base_path}')
        self.base_path = base_path
        self.albums = []
        self.__load_albums(self.base_path)
        
        
    def __load_albums(self, path):
        is_album = False
        for p in os.listdir(path):
            new_path = os.path.join(path, p)
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