from uc3m_travel.attributes.attributes import Attribute
from uc3m_travel.hotel_management_exception import HotelManagementException

class Dni(Attribute):
    """Definition of attribute Dni"""

    def __init__(self, attr_value):
        """Definition of attribute Dni init"""
        self._validation_pattern = r"^[0-9]{8}[A-Z]{1}$"
        self._error_message = "Invalid IdCard format"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        super()._validate(attr_value)
        characters = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
             "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
             "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
             "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        value = int(attr_value[0:8])
        reminder = str(value % 23)
        if characters[reminder] != attr_value[8]:
            raise HotelManagementException("Invalid IdCard letter")
        return attr_value[8] == characters[reminder]