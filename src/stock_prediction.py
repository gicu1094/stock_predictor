import os
import random
import csv

import utilities.utilities as util

class StockPrediction:
    
    def __init__(self, recomended_number_of_files):
            self.__number_of_files_for_each_stock = recomended_number_of_files
            self.__stocks_to_be_processed = []
        
    def initialize(self):
        """
        Initialize StockPrediction object.
        """
        parent_directory = "input_data"
        try:
            stocks_list = self.__get_list_of_stocks_folders(parent_directory)
            self.__stocks_to_be_processed = self.__get_stocks_list_to_be_processed(stocks_list, self.__number_of_files_for_each_stock)
            return True
        except Exception as e:
            print(f"Object initializing error occured: {e}")
            return False

    def get_stocks_to_be_processed(self):
        return self.__stocks_to_be_processed

    def get_10_consecutive_data_points_from_file(self, file_name):
        """
        For each file provided, returns 10 consecutive data points starting from a random timestamp.

        Input Params:
        file_name - path to a file to be processed

        Output:
        None - in case file cannot be processed
        file_data - a list of 10 consecutive rows(every row is mapped to a dictionary),
                    from a random timestamp.

        """
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
        """
        Predicts the next 3 values of prices for provided list, then it writes the output .csv file

        Input Params:
        stock_list - list of dictionaries.

        Output:
        A .csv file in output_data folder if no exceptions occurs.

        """
        if stock_list is None or not stock_list:
            return
        
        try:
            #this is my prediction algorithm for n+1
            price1 = util.get_second_max_price(stock_list)
            last_row = stock_list[-1]
            stock_id = last_row['stock-id']
            last_timestamp = last_row['timestamp']
            next_day1 = util.get_next_day(last_timestamp)
            row_to_add1 = {
                'stock-id' : stock_id,
                'timestamp' : next_day1,
                'price' : price1
            }
            stock_list.append(row_to_add1)
        except Exception as e:
            print(f"Error occureed while predictin n+1 price: {e}")

        try:
            #predict second price
            next_day2 = util.get_next_day(next_day1)
            last_2_rows = stock_list[-2:]
            #this is what I understood from requirements
            #diff_between_last_2 = abs(last_2_rows[0]['price'] - last_2_rows[1]['price'])
            #half_diff = diff_between_last_2 / 2

            #this is my prediction algorithm for n+2
            diff_between_last_2 = abs(last_2_rows[0]['price'] - last_2_rows[1]['price'])
            if diff_between_last_2 != 0:
                half_diff = diff_between_last_2 / 2
                price2 = last_2_rows[1]['price'] + half_diff 
            else:
                price2 = (stock_list[0]['price'] + stock_list[-1]['price'])/2
               
            row_to_add2 = {
                'stock-id' : stock_id,
                'timestamp' : next_day2,
                'price' : price2
            }
            stock_list.append(row_to_add2)
        except Exception as e:
            print(f"Error occureed while predictin n+2 price: {e}")

        try:
            ##predict third price
            next_day3 = util.get_next_day(next_day2)
            
            #this is what I understood from requirements
            #last_2_rows = stock_list[-2:]
            #diff_between_last_two = abs(last_2_rows[0]['price'] - last_2_rows[1]['price'])
            #quarter_diff = diff_between_last_two / 4

            #this is my prediction algorithm for n+3
            sum_of_last_five = 0.0
            for row in stock_list[-5:]:
                sum_of_last_five += row['price']
            price3 = sum_of_last_five/5
            row_to_add3 = {
                'stock-id' : stock_id,
                'timestamp' : next_day3,
                'price' : price3
            }
            stock_list.append(row_to_add3)
        except Exception as e:
            print(f"Error occureed while predictin n+3 price: {e}")
        
        print(stock_list)
        util.write_output_csv(stock_list)


    def __get_list_of_stocks_folders(self, input_data_path):
        """
        This is used to get list of stock from input data folder.
        Reads all folders names from a specified parent folder.

        Input Params:
        input_data_path - parest folder of stocks folders

        Output:
        stocks_list - a list of folders paths.
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
        list_of_files_to_be_processed - a list of files paths, for which, stocks should be predicted.

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
