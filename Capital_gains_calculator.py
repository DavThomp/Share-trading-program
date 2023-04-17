"""
A1 challenge
David Thompson
"""


import csv
import datetime
from operator import itemgetter


SAMPLE_TRADES_1 = [['PEAR', 'b', 100, 1000, datetime.date(2010, 1, 1)],
                   ['PEAR', 's', 50, 1500, datetime.date(2010, 12, 1)],
                   ['PEAR', 's', 20, 2000, datetime.date(2015, 1, 1)]]

SAMPLE_GAINS_LOSSES_1 = [['PEAR', 1000.0, datetime.date(2010, 12, 1)],
                         ['PEAR', 900.0, datetime.date(2015, 1, 1)]]

SAMPLE_TRADES_2 = [['PEAR', 'b', 100, 1000, datetime.date(2010, 1, 1)],
                   ['PEAR', 'b', 100, 3000, datetime.date(2010, 12, 1)],
                   ['PEAR', 's', 150, 15000, datetime.date(2011, 6, 30)],
                   ['PEAR', 's', 30, 600, datetime.date(2020, 1, 1)]]

SAMPLE_GAINS_LOSSES_2 = [['PEAR', 8000.0, datetime.date(2011, 6, 30)],
                         ['PEAR', -300.0, datetime.date(2020, 1, 1)]]


def calculate_taxable_gains_and_losses(trading_data):
    # Sort the trading data so sales and cost_based will be oldest first.
    trading_data.sort(key=itemgetter(0))

    # Create a sales list and a cost list.
    sales = []
    costs = []
    for trade in trading_data:
        if trade[1] == "s":
            sales.append([trade[0], trade[2], trade[3], trade[4]])
        else:
            costs.append([trade[0], trade[2], trade[3], trade[4]])

    # For each sale iterate through the cost list to calculate a capital gain or loss.
    i = 0
    popped = 0
    capital_gains_or_losses = []
    for sale in sales:
        ticker = sale[0]
        sale_value = sale[2]
        sale_quantity = sale[1]
        sale_quantity_remaining = sale[1]
        sale_date = sale[3]
        capital_gain_or_loss_total = 0
        while sale_quantity_remaining > 0:
            for cost in costs:
                if ticker == cost[0]:
                    cost_value = cost[2]
                    cost_quantity = cost[1]
                    cost_date = cost[3]
                    if sale_quantity_remaining >= cost_quantity:
                        cost_base = cost_value
                        costs.pop(i - popped)
                        popped = popped + 1
                        i = i + 1
                        capital_gain_or_loss_portion = sale_value / sale_quantity * cost_quantity - cost_base
                    else:
                        cost_base = cost_value / cost_quantity * sale_quantity_remaining
                        cost_quantity_remaining = cost_quantity - sale_quantity_remaining
                        cost[1] = cost_quantity_remaining
                        cost_value_remaining = cost_value / cost_quantity * cost_quantity_remaining
                        cost[2] = cost_value_remaining
                        capital_gain_or_loss_portion = \
                            sale_value / sale_quantity * (cost_quantity - cost_quantity_remaining) - cost_base
                    is_discounted = is_capital_gain_discounted(capital_gain_or_loss_portion, sale_date, cost_date)
                    if is_discounted:
                        capital_gain_or_loss_portion = capital_gain_or_loss_portion * 0.5
            capital_gain_or_loss_total = capital_gain_or_loss_total + capital_gain_or_loss_portion
            sale_quantity_remaining = sale_quantity_remaining - cost_quantity
        capital_gains_or_losses.append([ticker, capital_gain_or_loss_total, sale_date])
    return capital_gains_or_losses


def is_capital_gain_discounted(gain_or_loss, sale_date, cost_date):
    if gain_or_loss < 0:
        return False
    else:
        days_held = sale_date - cost_date
        if days_held.days > 365:
            return True
        else:
            return False


def test_calculate_taxable_gains_and_losses(test_data, expected_result):
    print(f"Test case {test_data}")
    actual_result = calculate_taxable_gains_and_losses(test_data)
    if actual_result != expected_result:
        print("Test failed.")
        print(f"Expected {expected_result}.")
        print(f"Actual result {actual_result}.")
    else:
        print("Test passed.")


if __name__ == '__main__':
    test_calculate_taxable_gains_and_losses(SAMPLE_TRADES_1, SAMPLE_GAINS_LOSSES_1)
    test_calculate_taxable_gains_and_losses(SAMPLE_TRADES_2, SAMPLE_GAINS_LOSSES_2)





