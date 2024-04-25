from uc3m_travel.attributes.attributes import Attribute
from uc3m_travel.hotel_management_exception import HotelManagementException

class CreditCard(Attribute):
    """Definition of attribute Credit Card"""

    def __init__(self, attr_value):
        """Definition of attribute Credit Card init"""
        self._validation_pattern = r"^[0-9]{16}"
        self._error_message = "Invalid credit card format"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        super()._validate(attr_value)
        def digits_of(number):
            return [int(digit) for digit in str(number)]
        
        digits = digits_of(attr_value)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for digit in even_digits:
            checksum += sum(digits_of(digit * 2))
        if not checksum % 10 == 0:
            raise HotelManagementException("Invalid credit card number (not luhn)")
        return attr_value