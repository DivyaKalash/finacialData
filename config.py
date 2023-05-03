import configparser

config = configparser.ConfigParser()

config.add_section("company_tickers")

#here we need to add company tickers to get data
config.set("company_tickers", "tickers", "AMZN, AB, IBM, INTC, MSFT")

with open("config.ini", 'w') as example:
    config.write(example)
