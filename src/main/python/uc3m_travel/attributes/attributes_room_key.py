from uc3m_travel.attributes.attributes import Attribute

class RoomKey(Attribute):
    """Definition of attribute RoomKey"""

    def __init__(self, attr_value):
        """Definition of attribute RoomKey init"""
        self._validation_pattern = r'^[a-fA-F0-9]{64}$'
        self._error_message = "Invalid room key format"
        self._attr_value = self._validate(attr_value)