import os
import random
import csv

from utilities.utilities import get_next_day
from utilities.utilities import write_output_csv
from utilities.utilities import get_second_max_price

class StockPrediction:
    
    def __init__(self, parent_directory):
            self.__parent_directory = parent_directory
            self.__stocks_to_be_processed = []
        
    def initialize(self):
        try:
            stocks_list = self.__get_list_of_stocks_folders(self.__parent_directory)
            self.__stocks_to_be_processed = self.__get_stocks_list_to_be_processed(stocks_list, 2)
            return True
        except Exception as e:
            print(f"Object initializing error occured: {e}")
            return False

    def get_stocks_to_be_processed(self):
        return self.__stocks_to_be_processed

    def get_10_consecutive_data_points_from_file(self, file_name):
        try:
            with open(file_name, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file, fieldnames=['stock-id', 'timestamp', 'price'])
                file_data = []
                for row in csv_reader:
                    try:
                        file_data.append({
                            'stock-id': row['stock-id'],
                            'timestamp': row['timestamp'],
                            'price': float(row['price'])
                        })
                    except Exception as e:
                        #skip the file if the format is wrong
                        print(f"Error parsing row in file {file_name}: {e}")
                        return None
                
                #skip processing the files with less than 10 records
                if len(file_data) < 10:
                    print(f"Skip file {file_name} because it has less than 10 records!")
                    return None
                    
        except Exception as e:
            print(f"Error reading file {file_name}: {e}")
            return None
        
        #get the random timestamp from file
        try:
            random_timestamp_idx = random.randint(0, len(file_data)-10)
            print(random_timestamp_idx)
            return file_data[random_timestamp_idx:random_timestamp_idx+10]
        except Exception as e:
             print(f"Error extracting rows: {e}")
             return None


    def predict_next_3_values_for_stock(self, stock_list):

        if stock_list is None or not stock_list:
            return
        #predict first price
        first_predicted_price = get_second_max_price(stock_list)
        last_row = stock_list[-1]
        stock_id = last_row['stock-id']
        last_timestamp = last_row['timestamp']
        next_day1 = get_next_day(last_timestamp)
        row_to_add1 = {
            'stock-id' : stock_id,
            'timestamp' : next_day1,
            'price' : first_predicted_price
        }
        stock_list.append(row_to_add1)

        #predict second price
        next_day2 = get_next_day(next_day1)
        last_2_rows = stock_list[-2:]
        #this is what I understood from requirements
        #diff_between_last_2 = abs(last_2_rows[0]['price'] - last_2_rows[1]['price'])
        #half_diff = diff_between_last_2 / 2

        #this is my prediction algorithm for n+2
        diff_between_last_2 = abs(last_2_rows[0]['price'] - last_2_rows[1]['price'])
        half_diff = diff_between_last_2 / 2
        price2 = last_2_rows[1]['price'] + half_diff
        row_to_add2 = {
            'stock-id' : stock_id,
            'timestamp' : next_day2,
            'price' : round(price2, 2)
        }
        stock_list.append(row_to_add2)

        ##predict third price
        next_day3 = get_next_day(next_day2)
        last_2_rows = stock_list[-2:]
        #this is what I understood from requirements
        #diff_between_last_two = abs(last_2_rows[0]['price'] - last_2_rows[1]['price'])
        #quarter_diff = diff_between_last_two / 4

        #this is my prediction algorithm for n+2
        diff_between_last_two = abs(last_2_rows[0]['price'] - last_2_rows[1]['price'])
        quarter_diff = diff_between_last_two / 4
        price3 = last_2_rows[1]['price'] - quarter_diff
        row_to_add3 = {
            'stock-id' : stock_id,
            'timestamp' : next_day3,
            'price' : round(price3, 2)
        }
        stock_list.append(row_to_add3)
        
        print(stock_list)
        write_output_csv(stock_list)


    def __get_list_of_stocks_folders(self, input_data_path):
        """
        This is used to get list of stock from input data folder.
        Reads all folders names from a specified parent folder.

        Input Params:
        input_data_path - parest folder of stocks folders
        """
        if not os.path.exists(input_data_path):
            raise FileNotFoundError(f"The directory '{input_data_path}' does not exist.")
        
        stocks_list = []
        for stock in os.listdir(input_data_path):
            try: 
                stock_name = os.path.join(input_data_path, stock)
                if os.path.isdir(stock_name):
                    stocks_list.append(stock_name)
            except Exception as e:
                print(f"Error processing stock {stock_name} : {e}")

        return stocks_list

    def __get_stocks_list_to_be_processed(self, stocks_list, files_to_process_from_each_folder):
        '''
        This helps to get only the files for which we have to predict the next 3 rows of stock.

        Input Params:
        stocks_list - a list of folders that contains .csv files
        files_to_process_from_each_folder - number of files to be processed from each folder

        Output:
        list_of_files_to_be_processed - a list of files for which stoks should be predicted

        '''
        list_of_files_to_be_processed = []
        for stock_folder in stocks_list:
            try:
                processed_files = 0
                for file_name in os.listdir(stock_folder):
                    if file_name.endswith('.csv'):
                        file_path = os.path.join(stock_folder, file_name)
                        processed_files += 1
                        list_of_files_to_be_processed.append(file_path)
                    else:
                        print(f"Wrong file extention: {file_name}")
                    
                    if(processed_files == files_to_process_from_each_folder):
                        break
            except Exception as e:
                print(f"Error accessing folder {stock_folder}: {e}")

        return list_of_files_to_be_processed
