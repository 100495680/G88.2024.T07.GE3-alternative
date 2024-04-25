from uc3m_travel.attributes.attributes import Attribute

class PhoneNumber(Attribute):
    """Definition of attribute RoomKey"""

    def __init__(self, attr_value):
        """Definition of attribute RoomKey init"""
        self._validation_pattern = r"^(\+)[0-9]{9}"
        self._error_message = "Invalid phone number format"
        self._attr_value = self._validate(attr_value)