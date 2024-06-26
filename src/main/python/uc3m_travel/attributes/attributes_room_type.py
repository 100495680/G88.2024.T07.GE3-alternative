from uc3m_travel.attributes.attributes import Attribute

class RoomType(Attribute):
    """Definition of attribute RoomType"""

    def __init__(self, attr_value):
        """Definition of attribute RoomType init"""
        self._validation_pattern = r"(SINGLE|DOUBLE|SUITE)"
        self._error_message = "Invalid roomtype value"
        self._attr_value = self._validate(attr_value)