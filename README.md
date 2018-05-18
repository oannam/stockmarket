#StocksMarket

##stockscli

stockscli is a client line interface to operate on stocks.

Python2.7

In order to run stockscli:

```
python bootstrapper.py

```

Usage:

```
# to see existing commands
(stockscli)help
(stockscli)?
Documented commands (type help <topic>):
========================================
calculate  exit  help  load  record  selectsym  showdb  showsym

# help or ? before command to see explanation for command
(stockscli)help calculate

        Calculates different formulas for available stocks.
        Example:
            calculate show # to see available formulas with details
            calculate formula_name [args] # calculate a formula with given args

(stockscli)help exit

        Exits StocksCLI. All the data in the simulated database will be gone.

(stockscli)help load

        Loads data from given file.
        Example: load ./sample_data.yml
(stockscli)help record

        Records a trade for the currently selected stock symbol.
        Please quantity of shares, buy or sell indicator and traded price.
        Example: record 2 buy 200
                record 4 sell 100

(stockscli)help selectsym

        Select current stock symbol to calculate formulas on.
        Example: selectsym ALE

(stockscli)help showdb

        Shows existing simulated database records.
        Example:
            showdb # displays all info in database
            showdb [arg] # displays info about a given stock symbol

(stockscli)help showsym

        Shows existing stock symbols to select from.
        Shows current selected stock symbol.
        
(stockscli)help exit

        Exits StocksCLI. All the data in the simulated database will be gone.
        
# load initial data base in yml format
(stockscli)load stocks/sample_data.yml
Loading data from yaml file: sample_data.yml

# use showdb command at any time to see the simulated database

(stockscli)showdb
ALE: {fixed_dividend: null, last_dividend: 23, par_value: 60, type: Common}
GIN: {fixed_dividend: 0.02, last_dividend: 8, par_value: 100, type: Common}
JOE: {fixed_dividend: null, last_dividend: 13, par_value: 250, type: Common}
POP: {fixed_dividend: null, last_dividend: 8, par_value: 100, type: Common}
TEA: {fixed_dividend: null, last_dividend: 0, par_value: 100, type: Common}

# see existing stocks symbols loaded from the simulated data base

(stockscli)showsym
Available stock symbols: ['TEA', 'ALE', 'JOE', 'POP', 'GIN']
Currently selected stock symbol: None

# select a certain stock symbol to do operations on

(stockscli)selectsym GIN
(stockscli)showsym
Available stock symbols: ['TEA', 'ALE', 'JOE', 'POP', 'GIN']
Currently selected stock symbol: GIN

# start recording trades on the selected symbol with record

(stockscli)record 6 buy 78
(stockscli)record 9 sell 56

# see the recordings in the simulated data base

(stockscli)showdb GIN
fixed_dividend: 0.02
last_dividend: 8
par_value: 100
records:
- [1526582911.244724, 6, buy, 78.0]
- [1526582917.294051, 9, sell, 56.0]
type: Common

(stockscli)showdb
ALE: {fixed_dividend: null, last_dividend: 23, par_value: 60, type: Common}
GIN:
  fixed_dividend: 0.02
  last_dividend: 8
  par_value: 100
  records:
  - [1526582911.244724, 6, buy, 78.0]
  - [1526582917.294051, 9, sell, 56.0]
  type: Common
JOE: {fixed_dividend: null, last_dividend: 13, par_value: 250, type: Common}
POP: {fixed_dividend: null, last_dividend: 8, par_value: 100, type: Common}
TEA: {fixed_dividend: null, last_dividend: 0, par_value: 100, type: Common}

# calculate different formulas on the selected stock symbol or on the entire database

(stockscli)calculate show
['dividend_yield', 'gbce_all_share_index', 'pe_ratio', 'volum_weighted_stock_price']
(stockscli)calculate dividend_yield 65
0.123076923077
(stockscli)calculate pe_ratio 78
3900.0
(stockscli)calculate gbce_all_share_index
2184.0
(stockscli)calculate volum_weighted_stock_price
64.8

#continue by selecting another stock symbol ...

```

Unit tests only created for formulas.py module.
See README.md in test folder in order to run unit tests.