import unittest

import utilities.utilities as util

class TestUtilities(unittest.TestCase):
    def test_get_next_day(self):
        wrong_format_date = "01-15-2025"
        next_day_wrong_format = util.get_next_day(wrong_format_date)
        self.assertEqual(next_day_wrong_format, None)

        date = '01-07-2025'
        next_day = util.get_next_day(date)
        self.assertEqual(next_day, '02-07-2025')

        date2 = '31-10-2025'
        next_day2 = util.get_next_day(date2)
        self.assertEqual(next_day2, '01-11-2025')

        date3 = '31-12-2025'
        next_day3 = util.get_next_day(date3)
        self.assertEqual(next_day3, '01-01-2026')

        date4 = '28-02-2024'
        next_day4 = util.get_next_day(date4)
        self.assertEqual(next_day4, '29-02-2024')

    def test_second_max_price(self):
        list1 = [{'stock-id': 'FLTR', 'timestamp': '29-10-2023', 'price': 17152.05},
                 {'stock-id': 'FLTR', 'timestamp': '30-10-2023', 'price': 17375.03},
                 {'stock-id': 'FLTR', 'timestamp': '31-10-2023', 'price': 17583.53},
                 {'stock-id': 'FLTR', 'timestamp': '01-11-2023', 'price': 17671.45},
                 {'stock-id': 'FLTR', 'timestamp': '02-11-2023', 'price': 17865.83},
                 {'stock-id': 'FLTR', 'timestamp': '03-11-2023', 'price': 18008.76}]
        
        second_max1 = util.get_second_max_price(list1)
        self.assertEqual(second_max1, 17865.83)

        #test the case where we have the maximum 2 times
        list2 = [{'stock-id': 'FLTR', 'timestamp': '29-10-2023', 'price': 17152.05},
                 {'stock-id': 'FLTR', 'timestamp': '30-10-2023', 'price': 17375.03},
                 {'stock-id': 'FLTR', 'timestamp': '31-10-2023', 'price': 17583.53},
                 {'stock-id': 'FLTR', 'timestamp': '01-11-2023', 'price': 18008.76},
                 {'stock-id': 'FLTR', 'timestamp': '02-11-2023', 'price': 15865.83},
                 {'stock-id': 'FLTR', 'timestamp': '03-11-2023', 'price': 18008.76}]
        
        #test the case where there are multiple second_max values
        list3 = [{'stock-id': 'FLTR', 'timestamp': '29-10-2023', 'price': 17152.05},
                 {'stock-id': 'FLTR', 'timestamp': '30-10-2023', 'price': 17152.05},
                 {'stock-id': 'FLTR', 'timestamp': '31-10-2023', 'price': 17152.05},
                 {'stock-id': 'FLTR', 'timestamp': '01-11-2023', 'price': 17152.05},
                 {'stock-id': 'FLTR', 'timestamp': '02-11-2023', 'price': 17152.05},
                 {'stock-id': 'FLTR', 'timestamp': '03-11-2023', 'price': 17152.11}]

        second_max3 = util.get_second_max_price(list3)
        self.assertEqual(second_max3, 17152.05)

        #test the case where there are multiple second_max values
        list4 = [{'stock-id': 'FLTR', 'timestamp': '29-10-2023', 'price': 17152.05},
                 {'stock-id': 'FLTR', 'timestamp': '30-10-2023', 'price': 17152.05},
                 {'stock-id': 'FLTR', 'timestamp': '31-10-2023', 'price': 17152.05},
                 {'stock-id': 'FLTR', 'timestamp': '01-11-2023', 'price': 17152.05},
                 {'stock-id': 'FLTR', 'timestamp': '02-11-2023', 'price': 17152.05},
                 {'stock-id': 'FLTR', 'timestamp': '03-11-2023', 'price': 17152.05}]

        second_max4 = util.get_second_max_price(list4)
        self.assertEqual(second_max4, 17152.05)

    def test_write_csv_file(self):
        list1 = []
        is_file_written_correctly = util.write_output_csv(list1)
        self.assertEqual(is_file_written_correctly, False)

        #file with name test will be created in output_data
        list2 = [{'stock-id': 'test', 'timestamp': '29-10-2023', 'price': 18008.76},
                 {'stock-id': 'test', 'timestamp': '30-10-2023', 'price': 17583.53},
                 {'stock-id': 'test', 'timestamp': '31-10-2023', 'price': 17152.05},
                 {'stock-id': 'test', 'timestamp': '01-11-2023', 'price': 15865.835},
                 {'stock-id': 'test', 'timestamp': '02-11-2023', 'price': 17152.05},
                 {'stock-id': 'test', 'timestamp': '03-11-2023', 'price': 17152.11}]
        is_file_written_correctly2 = util.write_output_csv(list2)
        self.assertEqual(is_file_written_correctly2, True)
if __name__ == "__main__":
    unittest.main()