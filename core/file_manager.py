import os, json, pickle
from core import settings
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor

class FileManager:

    def __init__(self, filename):
        self.__filename = filename

    def write_to_json(self, data):
        file_path = os.path.join(settings.MEDIA_ROOT, self.__filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)

    def add_to_json(self, data):
        file_path = os.path.join(settings.MEDIA_ROOT, self.__filename)
        with open(file_path, 'a', encoding='utf-8') as file:
            x = json.dumps(data, indent=2, ensure_ascii=False)
            file.write(x + ',\n')

    def read_from_json(self):
        file_path = os.path.join(settings.MEDIA_ROOT, self.__filename)
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return None
        
    def read_from_pkl(self) -> StandardScaler | MLPRegressor:
        file_path = os.path.join(settings.MEDIA_ROOT, self.__filename)
        try:
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return None