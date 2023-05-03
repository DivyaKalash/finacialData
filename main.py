#imports
import pandas as pd
import datetime
import time
import yfinance as yf
import mysql.connector
import configparser
from flask import Flask, jsonify, request

#getting data from config file(config.ini)
config_data = configparser.ConfigParser()
config_data.read("config.ini")
company_tickers = config_data["company_tickers"]
ticker_symbols = company_tickers.get('tickers')
ticker_symbol = ticker_symbols.split(",")
print(ticker_symbol)

#inserting data in sql table of name stockData based on the data of the listed companies in config file from date 01/01/23 to 30/04/23
updated = []
Updated = []
i = 0
start = datetime.datetime(2023,1,1)
end = datetime.datetime(2023, 4, 30)

start_time = time.time()

for i in ticker_symbol:
    print(i)
    data = yf.download(i, start, end)
    data.insert(0, 'TickerSymbol', i)
    updated = pd.DataFrame(data)
    Updated.append(updated)
    stockdata = pd.concat(Updated, axis = 0)


print(stockdata)
stockdata.reset_index(level=0, inplace=True)


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Mysql1#",
  database="tsworks"
)

mycursor = mydb.cursor()

insert_query = 'INSERT INTO stockData(TickerSymbol, TradeDate, st_open, st_high, st_close, st_low, Volume, Adj_close) values(%s, %s, %s, %s, %s, %s, %s, %s)'
for index,row in stockdata.iterrows():
    mycursor.execute(insert_query,(row['TickerSymbol'], row['Date'], row['Open'], row['High'], row['Close'], row['Low'], row['Volume'], row['Adj Close']))

mydb.commit()
mydb.close()

#function for get stock data based on date
def get_stock_ondate(datee):
    stock_dets = []
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="Mysql1#",
      database="tsworks"
    )
    # print("running")
    mycursor = mydb.cursor()
    query = "select * from stockData where TradeDate = %s"
    # dat = ("datee")
    print(type(datee))
    mycursor.execute(query, (datee,))

    myresult = mycursor.fetchall()
    print(myresult)

    for x in myresult:
        print(x)
        stock_dets.append(x)
    return stock_dets

#function for get data based on company ticker
def get_stock_oncompany(tickle):
    stock_dets = []
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="Mysql1#",
      database="tsworks"
    )
    # print("running")
    mycursor = mydb.cursor()
    query = "select * from stockData where TickerSymbol = %s"
    # dat = ("datee")

    mycursor.execute(query, (tickle,))

    myresult = mycursor.fetchall()
    print(myresult)

    for x in myresult:
        print(x)
        stock_dets.append(x)
    return stock_dets

#function to get stock data based on date and company ticker
def get_stock_ondate_and_company(datee, trickle):
    stock_dets = []
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="Mysql1#",
      database="tsworks"
    )
    # print("running")
    mycursor = mydb.cursor()
    query = "select * from stockData where TickerSymbol = %s and TradeDate = %s"
    # dat = ("datee")
    # print(type(datee))
    mycursor.execute(query, (trickle,datee))

    myresult = mycursor.fetchall()
    print(myresult)

    for x in myresult:
        print(x)
        stock_dets.append(x)
    return stock_dets

#update rows of the table based on date and company ticker with new values
def update_stock_ondate_and_company(datee, trickle, newTrickle, newDate, newOpen, newClose, newLow, newHigh, newVolume, newAdjClose):

    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="Mysql1#",
      database="tsworks"
    )
    # print("running")
    mycursor = mydb.cursor()
    query = "update stockData set TickerSymbol = %s, TradeDate = %s, st_open = %s, st_high = %s, st_low = %s, st_close = %s, Volume = %s, Adj_close = %s where TickerSymbol = %s and TradeDate = %s"
    # dat = ("datee")
    # print(type(datee))
    mycursor.execute(query, (newTrickle,newDate,newOpen,newHigh,newLow, newClose, newVolume, newAdjClose, trickle,datee))

    mydb.commit()

#flask apis
app = Flask(__name__)

@app.route("/get_all_company_stockdata_ondate", methods=["GET"])
def get_all_company_stockdata_ondate():
    json = request.get_json()
    stock_datas = get_stock_ondate(json["date"])
    response = {"stock_datas": stock_datas}
    return jsonify(response), 201

@app.route("/get_all_company_stockdata_oncompany", methods=["GET"])
def get_all_company_stockdata_oncompany():
    json = request.get_json()
    stock_datas = get_stock_oncompany(json["trickle"])
    response = {"stock_datas": stock_datas}
    return jsonify(response), 201

@app.route("/get_all_company_stockdata_ondate_and_company", methods=["GET"])
def get_all_company_stockdata_ondate_and_company():
    json = request.get_json()
    stock_datas = get_stock_ondate_and_company(json["date"],json["trickle"])
    response = {"stock_datas": stock_datas}
    return jsonify(response), 201

@app.route("/update_company_stockdata_ondate_and_company", methods=["PATCH"])
def update_company_stockdata_ondate_and_company():
    json = request.get_json()
    update_stock_ondate_and_company(json["date"],json["trickle"],json["newTrickle"],json["newDate"],json["newOpen"],json["newHigh"],json["newLow"],json["newClose"],json["newVolume"],json["newAdjClose"])
    response = {"message": "updated successfully!"}
    return jsonify(response), 201

app.run(host="0.0.0.0", port=2707)





