import unittest

from src.stock_prediction import StockPrediction

class TestStockPrediction(unittest.TestCase):
    def test_obj_initialization(self):
        folder_path1 = "input_data"
        obj = StockPrediction(folder_path1)
        self.assertEqual(obj.initialize(), True)

        folder_path2 = "wrong_path"
        obj2 = StockPrediction(folder_path2)
        self.assertEqual(obj2.initialize(), False)
    
    def test_get_10_consecutive_data_points_from_file(self):

        #test basic case
        obj = StockPrediction("tests\\input_files_for_testing")
        list1 = obj.get_10_consecutive_data_points_from_file("tests\\input_files_for_testing\\test1.csv")
        self.assertEqual(len(list1), 10)

        #test with empty file
        list2 = []
        if obj.get_10_consecutive_data_points_from_file("tests\\input_files_for_testing\\test2.csv") != None:
            list2 = obj.get_10_consecutive_data_points_from_file("tests\\input_files_for_testing\\test2.csv")
        self.assertEqual(len(list2), 0)

        #test with a file which has wrong formated data inside
        list3 = []
        if obj.get_10_consecutive_data_points_from_file("tests\\input_files_for_testing\\test3.csv") != None:
            list3 = obj.get_10_consecutive_data_points_from_file("tests\\input_files_for_testing\\test3.csv")
        self.assertEqual(len(list3), 0)

        #test with a file which has less than 10 rows
        list4 = []
        if obj.get_10_consecutive_data_points_from_file("tests\\input_files_for_testing\\test4.csv") != None:
            list4 = obj.get_10_consecutive_data_points_from_file("tests\\input_files_for_testing\\test4.csv")
        self.assertEqual(len(list4), 0)


