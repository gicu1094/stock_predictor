import os
import csv
from datetime import datetime, timedelta

def get_next_day(date):
    '''
    Return the next valid date.
    
    '''
    try:
        date_object = datetime.strptime(date, '%d-%m-%Y')
        next_day = date_object + timedelta(days=1)
        return next_day.strftime('%d-%m-%Y')
    except Exception as e:
        print(f"Invalid date format! : {e}")
        return None


def get_second_max_price(list_rows):
    first_max = float('-inf')
    second_max = float('-inf')
    for row in list_rows:
        price = row['price']
        if price > first_max:
            second_max = first_max
            first_max = price
        elif first_max > price > second_max:
            second_max = price
        
    if second_max == float('-inf'):
        raise ValueError("Not enough distinct prices!")

    return second_max
    
    
        
def write_output_csv(stock_list):
    if not stock_list:
        print("Error: Nothing to write!")
        return False
    
    try:
        output_folder = "output_data\\"
        stock_id = stock_list[0]['stock-id']
        os.makedirs(output_folder, exist_ok=True)
        output_csv_file = os.path.join(output_folder, f"{stock_id}_out.csv")
    except Exception as e:
        print(f"Unexpected error occured while creatin the output path: {e}")
        return False

    #this is done to have all the prices with 2 decimals
    #Example: 999.90 not 999.9
    try:
        for row in stock_list:
            row['price'] = "{:.2f}".format(row['price'])
    except Exception as e:
        print(f"Error while formating the price!")
        return False

    try:
        with open(output_csv_file, mode = 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['stock-id', 'timestamp', 'price'])
            writer.writerows(stock_list)
    except Exception as e:
        print(f"Error on writing in file {output_csv_file}: {e}")
        return False
    return True