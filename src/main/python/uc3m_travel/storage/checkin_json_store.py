from datetime import datetime

from freezegun import freeze_time

from uc3m_travel.hotel_reservation import HotelReservation
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.attributes.attributes_dni import Dni
from uc3m_travel.attributes.attributes_localizer import Localizer
from uc3m_travel.hotel_stay import HotelStay
from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_exception import HotelManagementException

class CheckinJsonStore(JsonStore):

    def __init__(self, file_name):
        super().__init__(file_name)
    def save_checkin(self):
        """manages the arrival of a guest with a reservation"""

        input_list = super().load_list_from_file()
        try:
            my_localizer = input_list["Localizer"]
            my_id_card = input_list["IdCard"]
        except:
            raise HotelManagementException("Error - Invalid Key in JSON")

        my_localizer = Localizer(my_localizer).value
        Dni(my_id_card).value
        stored_file = "store_reservation.json"
        self._file_name = JSON_FILES_PATH + stored_file
        find_status = super().find_item("_HotelReservation__localizer", my_localizer)
        if find_status == False:
            raise HotelManagementException("Error: localizer not found")
        print(find_status,my_id_card)
        if find_status["_HotelReservation__id_card"] != my_id_card:
            raise HotelManagementException("Error: Localizer is not correct for this IdCard")
        store_list = find_status
        reservation_date = datetime.fromtimestamp(store_list["_HotelReservation__reservation_date"])

        with freeze_time(reservation_date):
            new_reservation = HotelReservation(credit_card_number=store_list["_HotelReservation__credit_card_number"],
                                               id_card=store_list["_HotelReservation__id_card"],
                                               num_days=store_list[ "_HotelReservation__num_days"],
                                               room_type=store_list["_HotelReservation__room_type"],
                                               arrival=store_list["_HotelReservation__arrival"],
                                               name_surname=store_list["_HotelReservation__name_surname"],
                                               phone_number=store_list["_HotelReservation__phone_number"])

        if new_reservation.localizer != my_localizer:
            raise HotelManagementException("Error: reservation has been manipulated")

        # compruebo si hoy es la fecha de checkin
        reservation_format = "%d/%m/%Y"
        date_obj = datetime.strptime(store_list["_HotelReservation__arrival"], reservation_format)
        if date_obj.date() != datetime.date(datetime.utcnow()):
            raise HotelManagementException("Error: today is not reservation date")

        # genero la room key para ello llamo a Hotel Stay
        my_checkin = HotelStay(idcard=my_id_card, numdays=int(store_list["_HotelReservation__num_days"]),
                               localizer=my_localizer, roomtype=store_list["_HotelReservation__room_type"])

        checkin_store = "store_check_in.json"
        self._file_name = JSON_FILES_PATH + checkin_store
        data_list = super().load_list_from_file()

        if super().find_item("_HotelStay__room_key",my_checkin.room_key) == my_checkin.room_key:
            raise HotelManagementException("ckeckin  ya realizado")

        super().add_item(my_checkin.__dict__)

        super().save_list_to_file()

        return my_checkin.room_key
