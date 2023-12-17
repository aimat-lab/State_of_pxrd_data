from __future__ import annotations
import os
# from typing import Optional

# -------------------------------------------


class Folder:
    default_xrd_formats : list = ['raw', 'dif', 'gdf', 'dat', 'ras', 'cpi', 'txt', 'plv', 'xrdml']

    def __init__(self, path : str):
        self.path : str = path
        self.name : str = os.path.basename(path)
        self.sub_paths : list[str] = [os.path.join(self.path,name) for name in os.listdir(self.path)]

    def get_descendant_xrdfilepaths(self) -> list[str]:
        xrd_file_paths = []

        xrd_file_paths += self._get_children_xrdfilepaths()
        for folder_path in self._get_children_folderpaths():
            xrd_folder = Folder(path=folder_path)
            xrd_file_paths += xrd_folder.get_descendant_xrdfilepaths()

        return xrd_file_paths

    def get_children_xrdpaths(self):
        return self._get_children_xrdfilepaths() + self._get_children_folderpaths()

    def _get_children_xrdfilepaths(self) -> list[str]:
        return [path for path in self._get_children_filepaths() if self._get_path_is_xrd_file(path=path)]


    def _get_path_is_xrd_file(self, path : str):
        is_file = os.path.isfile(path)
        is_xrd_format = any([path.endswith(f'.{the_format}') for the_format in self.default_xrd_formats])
        return is_file and is_xrd_format


    # -------------------------------------------

    def _get_children_filepaths(self) -> list[str]:
        return [path for path in self.sub_paths if os.path.isfile(path)]

    def _get_children_folderpaths(self) -> list[str]:
        return [path for path in self.sub_paths if os.path.isdir(path)]