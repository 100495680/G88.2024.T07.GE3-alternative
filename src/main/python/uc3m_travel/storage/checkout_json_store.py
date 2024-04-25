import os
from datetime import datetime

from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.attributes.attributes_room_key import RoomKey

class CheckoutJsonStore(JsonStore):

    def __init__(self):
        self._file_name = ""

    def save_checkout(self, room_key: str) -> bool:
        """manages the checkout of a guest"""
        room_key = RoomKey(room_key).value
        # check thawt the roomkey is stored in the checkins file
        self._file_name = JSON_FILES_PATH + "store_check_in.json"
        if not os.path.isfile(self._file_name):
            raise HotelManagementException("Error: not found")

        find_status = super().find_item("_HotelStay__room_key", room_key)
        if find_status == False:
            raise HotelManagementException("Error: room key not found")

        today = datetime.utcnow().date()
        if datetime.fromtimestamp(find_status["_HotelStay__departure"]).date() != today:
            raise HotelManagementException("Error: today is not the departure day")

        self._file_name = JSON_FILES_PATH + "store_check_out.json"
        data_list = super().load_list_from_file()

        find_status = super().find_item("room_key", room_key)
        if find_status != False:
            raise HotelManagementException("Guest is already out")
        room_checkout = {"room_key": room_key, "checkout_time": datetime.timestamp(datetime.utcnow())}
        super().add_item(room_checkout)
        super().save_list_to_file()

        return True

