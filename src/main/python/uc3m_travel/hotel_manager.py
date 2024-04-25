"""Module for the hotel manager"""
import re
import json
from datetime import datetime
from uc3m_travel.storage.checkout_json_store import CheckoutJsonStore
from uc3m_travel.storage.checkin_json_store import CheckinJsonStore
from uc3m_travel.storage.reservation_json_store import ReservationJsonStore

"""Import Attributes from attributes folder"""
from uc3m_travel.attributes.attributes_dni import Dni
from uc3m_travel.attributes.attributes_localizer import Localizer
from uc3m_travel.attributes.attributes_phonenumber import PhoneNumber
from uc3m_travel.attributes.attributes_arrival_date import ArrivalDate
from uc3m_travel.attributes.attributes_credit_card import CreditCard
from uc3m_travel.attributes.attributes_room_key import RoomKey
from uc3m_travel.attributes.attributes_room_type import RoomType
from uc3m_travel.attributes.attributes_name_surname import NameSurname

from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_reservation import HotelReservation
from uc3m_travel.hotel_stay import HotelStay
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from freezegun import freeze_time

class HotelManager:
    class __HotelManager:
        """Class with all the methods for managing reservations and stays"""

        def __init__(self):
            pass

        def validate_credit_card(self, credit_card):
            """validates the credit card number using luhn altorithm"""
            return CreditCard(credit_card).value

        def validate_room_type(self, room_type):
            """validates the room type value using regex"""
            return RoomType(room_type).value

        def validate_arrival_date(self, arrival_date):
            """validates the arrival date format  using regex"""
            return ArrivalDate(arrival_date).value

        def validate_phonenumber(self, phone_number):
            """validates the phone number format  using regex"""
            return PhoneNumber(phone_number).value

        def validate_numdays(self, num_days):
            """validates the number of days"""
            try:
                days = int(num_days)
            except ValueError as exception:
                raise HotelManagementException("Invalid num_days datatype") from exception
            if (days < 1 or days > 10):
                raise HotelManagementException("Numdays should be in the range 1-10")
            return num_days

        @staticmethod
        def validate_dni(dni):
            """RETURN TRUE IF THE DNI IS RIGHT, OR FALSE IN OTHER CASE"""
            return Dni(dni).value

        def validate_name_surname(self, name_surname):
            return NameSurname(name_surname).value

        def validate_localizer(self, localizer):
            """validates the localizer format using a regex"""
            return Localizer(localizer).value

        def validate_roomkey(self, room_key):
            """validates the roomkey format using a regex"""
            return RoomKey(room_key).value

        def read_data_from_json(self, file):
            """reads the content of a json file with two fields: CreditCard and phoneNumber"""
            json_data = self.load_json(file)
            try:
                credit_card = json_data["CreditCard"]
                phone_number = json_data["phoneNumber"]
                reservation = HotelReservation(id_card="12345678Z",
                                               credit_card_number=credit_card,
                                               name_surname="John Doe",
                                               phone_number=phone_number,
                                               room_type="single",
                                               num_days=3,
                                               arrival="20/01/2024")
            except KeyError as exception:
                raise HotelManagementException("JSON Decode Error - Invalid JSON Key") from exception
            CreditCard(credit_card)
            # Close the file
            return reservation

        # pylint: disable=too-many-arguments
        def room_reservation(self,
                             credit_card: str,
                             name_surname: str,
                             id_card: str,
                             phone_number: str,
                             room_type: str,
                             arrival_date: str,
                             num_days: int) -> str:
            """manges the hotel reservation: creates a reservation and saves it into a json file"""

            if not self.validate_dni(id_card):
                raise HotelManagementException("Invalid IdCard letter")

            room_type = self.validate_room_type(room_type)
            name_surname = self.validate_name_surname(name_surname)
            credit_card = self.validate_credit_card(credit_card)
            arrival_date = self.validate_arrival_date(arrival_date)
            num_days = self.validate_numdays(num_days)
            phone_number = self.validate_phonenumber(phone_number)
            my_reservation = HotelReservation(id_card=id_card,
                                              credit_card_number=credit_card,
                                              name_surname=name_surname,
                                              phone_number=phone_number,
                                              room_type=room_type,
                                              arrival=arrival_date,
                                              num_days=num_days)

            return ReservationJsonStore().save_reservation(my_reservation)

        def guest_arrival(self, file_input: str) -> str:
            """manages the arrival of a guest with a reservation"""
            return CheckinJsonStore(file_input).save_checkin()

        def guest_checkout(self, room_key: str) -> bool:
            """manages the checkout of a guest"""
            return CheckoutJsonStore().save_checkout(room_key)

        def load_json(self, file_store):
            try:
                with open(file_store, "r", encoding="utf-8", newline="") as file:
                    data_list = json.load(file)
            except FileNotFoundError as exception:
                raise HotelManagementException("Error: not found") from exception
            except json.JSONDecodeError as exception:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
            return data_list

    __instance =  None
    def __new__(cls):
        if not HotelManager.__instance:
            HotelManager.__instance = HotelManager.__HotelManager()
        return HotelManager.__instance
