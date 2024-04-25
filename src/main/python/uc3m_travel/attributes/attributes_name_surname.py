from uc3m_travel.attributes.attributes import Attribute

class NameSurname(Attribute):
    """Definition of attribute Name Surname"""

    def __init__(self, attr_value):
        """Definition of attribute Name Surname init"""
        self._validation_pattern = r"^(?=^.{10,50}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        self._error_message = "Invalid name format"
        self._attr_value = self._validate(attr_value)