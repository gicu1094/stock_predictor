# stock_predictor

# Description:
Stock Predictor is a Python application that, for each stock exchange, selects the specified number of files, and for each file provided, predict the next 3 values of stock price for that specific file.

# Prediction algorithm:
1. A random timestamp will be choosen from input file and from that timestamp, next 10 consecutive records will be selected.
2. Then using these 10 records, n+1, n+2 and n+3 price records will be predicted for each file(stock).

a) n+1_price --> the second max from 10 selected records(or max if all the values are the same)
After predictin first price, we add the record to the list, so it will influence the next prediction.

b) n+2_price --> 
if the difference between last 2 elements from the list is not 0 then
n+2_price = last_element + half difference between last 2 elements from the list
else if difference between last 2 elements from the list is 0 then
n+2_price = (first_elem_price + last_elem_price)/2

c) n+3 --> arithmetic average of last 5 elements from te list.

# Data & Inputs:
1. Sample data is provided as a set of folders, one for each exchange, .csv files. Each file has these 3 columns:
Stock-ID,Timestamp(dd-mm-yyyy),stock_price_value
2. Input parameter to solution is the recommended number of files to be sampled for each stock exchange. Valit inputs are 1 or 2.

# Output format:
One .csv output file for each file processed. Each .csv file should have 3 columns on each row as shown below.
Timestamp & stock price have same format as in input file.
Stock-ID,Timestamp-1,stock price 1
..
Stock-ID,Timestamp-n,stock price n
Stock-ID,Timestamp-n+1,stock price n+1
Stock-ID,Timestamp-n+2,stock price n+2
Stock-ID,Timestamp-n+3,stock price n+3

# Instalation:
1. Clone repository and go to project folder:
```bash
    git clone https://github.com/gicu1094/stock_predictor.git
    cd stock_predictor
```
2. Install python3 on your machine. Check on the internet how to do it specificaly for your type of OS.

# Usage:
1. All the stocks folders, for which you want to predict next values, has to be added in "input_data" folder.
2. To run the application just run the main.py file
```bash
For windows:
py -3 .\main.py

For linux:
python3 main.py
```
3. To check the output, after running the application, just check the "out_data" folder wich will be created after application was run. The folder will contain generated .csv files for each valid stock entry. The naming of the file is like this: "stock-id_out.csv", where stock-id is the stock-id from input files.

# Run unit tests:
```bash
python -m unittest discover tests
```

# Contact:
For questions or suggestions, feel free to reach out:
Email: cebotari.gheorghe@lseg.com
GitHub: gicu1094