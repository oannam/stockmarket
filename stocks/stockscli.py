"""
This module provides a CLI for enabling operations on stocks.
"""

from __future__ import print_function

import cmd
import time
import types
import yaml

from stocks.lib import formulas

AVAILABLE_FORMULAS = []
for fct in dir(formulas):
    if (
                isinstance(formulas.__dict__.get(fct), types.FunctionType)
            and fct.startswith('calculate')
    ):
        AVAILABLE_FORMULAS.append(fct.replace('calculate_', ''),)


class StocksCLI(cmd.Cmd):

    intro = """
        Welcome to StocksCLI. Type help or ? to list available operations
    """
    prompt = '(stockscli)'
    file = None

    simulated_db = {}

    current_selected_stock = None

    # basic commands

    def do_load(self, arg):
        """
        Loads data from given file.
        Example: load ./sample_data.yml
        """
        if arg:
            try:
                with open(arg, 'r') as stream:
                    try:
                        print('Loading data from yaml file: {0}'.format(arg))
                        self.simulated_db = yaml.load(stream)
                    except yaml.YAMLError as exc:
                        print(
                            'Encountered exception when loading given yaml file:\n{0}'.format(exc)
                        )
            except IOError:
                print('Wrong file path given.')
        else:
            print('Please provide a yaml file to load data from.')

    def do_exit(self, arg):
        """
        Exits StocksCLI. All the data in the simulated database will be gone.
        """
        print('Thank you for using SocksCLI. Exiting...')
        self.close()
        return True

    def do_selectsym(self, arg):
        """
        Select current stock symbol to calculate formulas on.
        Example: selectsym ALE
        """
        if arg and arg in self.simulated_db.keys():
            self.current_selected_stock = arg
        else:
            print('Selected symbol does not exist.')

    def do_showsym(self, arg):
        """
        Shows existing stock symbols to select from.
        Shows current selected stock symbol.
        """
        print('Available stock symbols: {0}'.format(self.simulated_db.keys()))
        print('Currently selected stock symbol: {0}'.format(self.current_selected_stock))

    def do_calculate(self, arg):
        """
        Calculates different formulas for available stocks.
        Example:
            calculate show # to see available formulas with details
            calculate formula_name [args] # calculate a formula with given args
        """
        if arg:
            length = len(arg.split(' '))
            if length == 2:
                formula, price = arg.split(' ')
                price_ok = True
                try:
                    price = float(price)
                except ValueError:
                    price_ok = False
                if price_ok:
                    if formula in ('dividend_yield', 'pe_ratio'):
                        if not self.simulated_db:
                            print('You have no data on which to perform operation.')
                            return
                        fct = 'calculate_' + formula
                        print(
                            formulas.__dict__[fct](
                                self.simulated_db[self.current_selected_stock],
                                price
                            )
                        )
                    else:
                        print('Please provide an available formula.')
                else:
                    print('Please provide a correct price.')
            elif length == 1:
                if arg == 'show':
                    print(AVAILABLE_FORMULAS)
                elif arg == 'volum_weighted_stock_price':
                    if not self.simulated_db or not self.current_selected_stock:
                        print('You have no data on which to perform operation.')
                        return
                    fct = 'calculate_' + arg
                    print(
                        formulas.__dict__[fct](
                            self.simulated_db[self.current_selected_stock].get('records', [])
                        )
                    )
                elif arg == 'gbce_all_share_index':
                    if not self.simulated_db:
                        print('You have no data on which to perform operation.')
                        return
                    fct = 'calculate_' + arg
                    print(formulas.__dict__[fct](self.simulated_db))
                elif arg in ('dividend_yield', 'pe_ratio'):
                    print('Please provide a price.')
                else:
                    print('Please provide the correct required paramaters.')
            else:
                print('Please provide the correct number of parameters.')
        else:
            print('Please provide one of the required parameters.')

    def do_record(self, arg):
        """
        Records a trade for the currently selected stock symbol.
        Please quantity of shares, buy or sell indicator and traded price.
        Example: record 2 buy 200
                record 4 sell 100
        """
        before_append = arg.split(' ')
        if len(before_append) == 3:
            if self.current_selected_stock:
                # check given params
                params_ok = True
                if before_append[1] not in ('buy', 'sell'):
                    print('The second parameter should be buy or sell.')
                    params_ok = False
                try:
                    int(before_append[0])
                except ValueError:
                    print('The first parameter should be an int.')
                    params_ok = False
                try:
                    float(before_append[2])
                except ValueError:
                    print('The third parameter should be a float')
                    params_ok = False
                if params_ok:
                    to_append = [
                        time.time(),
                        int(before_append[0]),
                        before_append[1],
                        float(before_append[2]),
                    ]
                    self.simulated_db[self.current_selected_stock].setdefault(
                        'records', []
                    ).append(to_append)
                else:
                    print('Please correct your parameters types.')
            else:
                print('Please select a stock symbol to add records to.')
        else:
            print('Please provide the required number of parameters.')

    def do_showdb(self, arg):
        """
        Shows existing simulated database records.
        Example:
            showdb # displays all info in database
            showdb [arg] # displays info about a given stock symbol
        """
        if arg:
            if arg in self.simulated_db.keys():
                print(yaml.dump(self.simulated_db[arg]))
            else:
                print('Given stock symbol as filter does not exist in simulated database.')
        else:
            print(yaml.dump(self.simulated_db))

    def close(self):
        if self.file:
            self.file.close()
            self.file = None
