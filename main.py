from src.stock_prediction import StockPrediction
from utilities.utilities import clean_up_output_data_folder

def main():
    
    while True:
        try:
            recomended_number_of_files = int(input("Enter the number of files to be processed from each stock: "))
            print(f"You entered {recomended_number_of_files}")
            if recomended_number_of_files in (1,2):
                break
            else:
                print(f"Invalid input. The input can be only 1 or 2")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    
    clean_up_output_data_folder("output_data")
    
    stock_predictor  = StockPrediction(recomended_number_of_files)
    if stock_predictor.initialize():
        stocks_to_process = stock_predictor.get_stocks_to_be_processed()
    else:
        return

    for file_name in stocks_to_process:
        list_of_data_points = stock_predictor.get_10_consecutive_data_points_from_file(file_name)
        stock_predictor.predict_next_3_values_for_stock(list_of_data_points)
    
    print("Check the output in output_data folder!")

if __name__ == "__main__":
    main()