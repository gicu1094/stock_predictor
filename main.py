from src.stock_prediction import StockPrediction

def main():
    parent_folder = "input_data"

    stock_predictor  = StockPrediction(parent_folder)
    if stock_predictor.initialize():
        stocks_to_process = stock_predictor.get_stocks_to_be_processed()
    else:
        return

    for file_name in stocks_to_process:
        list_of_data_points = stock_predictor.get_10_consecutive_data_points_from_file(file_name)
        stock_predictor.predict_next_3_values_for_stock(list_of_data_points)

if __name__ == "__main__":
    main()