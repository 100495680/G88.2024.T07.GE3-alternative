import unittest

from uc3m_travel import HotelManager


class MyTestCase(unittest.TestCase):
    '''TESTS CASES FOR THE HOTEL MANAGER SINGLETON'''

    def test_singleton_hotel_manager(self):
        manager1 = HotelManager()
        manager2 = HotelManager()
        manager3 = HotelManager()
        self.assertEqual(manager1, manager2)
        self.assertEqual(manager1, manager3)
        self.assertEqual(manager2, manager3)
