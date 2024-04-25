from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
import json


class JsonStore():
    """JsonStore class"""

    def __init__( self, file_name ):
        self._data_list = []
        self._file_name = file_name

    def save_list_to_file( self ):
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise HotelManagementException("Wrong file or file path") from ex

    def load_list_from_file( self ):
        try:
            with open(self._file_name, "r",encoding="utf-8",newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return self._data_list

    def add_item( self, item ):
        self._data_list.append(item)

    def find_item( self, key, value):
        self.load_list_from_file()
        for item in self._data_list:
            if item[key] == value:
                return item
        return False

    