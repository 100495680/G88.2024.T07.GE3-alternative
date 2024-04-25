from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
class ReservationJsonStore(JsonStore):

    def __init__(self):
        self._file_name = JSON_FILES_PATH + "store_reservation.json"
        super().__init__(self._file_name)


    def save_reservation(self, reservation_data):
        data_list = super().load_list_from_file()
        find_status = super().find_item("_HotelReservation__localizer", reservation_data.localizer)
        if find_status != False:
            raise HotelManagementException("Reservation already exists")
        find_status = super().find_item("_HotelReservation__id_card", reservation_data.id_card)
        if find_status != False:
            raise HotelManagementException("This ID card has another reservation")

        super().add_item(reservation_data.__dict__)

        super().save_list_to_file()

        return reservation_data.localizer