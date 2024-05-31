# %%

from typing import TextIO, Callable
import os

class Archiwith:
    def __init__(self, file_path: str) -> Callable:
        self.file_path: str = file_path
    
    def abrir(self, binari: bool = False) -> TextIO:
        if binari:
            self.file = open(self.file_path, 'rb')
        else:
            self.file = open(self.file_path, 'r')
        self._with = True
        return self.file
    
    def escribir(self, append: bool = False) -> TextIO:
        if append:
            self.file = open(self.file_path, 'a')
        else:
            self.file = open(self.file_path, 'w')
        self._with = True
        return self.file
    
    def leer(self) -> str:
        self.file = open(self.file_path, 'r').read()
        self._with = False
        return self.file

    def __exit__(self):
        if self._with:
            self.file.close()


class ObjectiFiles:
    def __init__(self, folder_path: str) -> object:
        """
        It converts the name files of the given path to attributes.
        """
        for item in os.listdir(folder_path):
            # Ignore folders and hidden files.
            if item[0] != '.' and os.path.isfile(f'{folder_path}/{item}'):
                print(f'converting {item}')
                # Avoid issues with attributes names by replacing special caracters by _.
                item = self._multi_replace(item, ('-','_'), (' ','_'), ('@','_'))
                name = f'f_{item.split('.')[-2]}__{item.split('.')[-1]}'
                setattr(self, name, item)
    
    def _multi_replace(self, text: str, *shifts) -> str:
        """
        Replace multiple substrings in a string.
        """
        for shift in shifts:
            text = text.replace(shift[0], shift[1])
        return text
# %%
