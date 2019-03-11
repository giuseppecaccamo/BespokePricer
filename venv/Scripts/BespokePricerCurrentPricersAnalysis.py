#Current pricers analysis

from datetime import datetime, timedelta
from collections import OrderedDict


def number_of_timeoccurrencies(lista):

    n=len(lista)
    dates = []
    for i, name in enumerate(lista):

        temp = lista[i].split(';')
        dates.append(temp[3])


    return n, dates


def dates_within_period(dates, days):

    #given a list of dates and a time period it returns a list containing the most recent dates with the time period
    temp_dates = [datetime.strptime(a,'%d-%b-%Y').date() for a in dates]
    unique_dates = list(OrderedDict.fromkeys(temp_dates))
    comparison_date = unique_dates[-1] - timedelta(days)
    index = [date >= comparison_date for date in unique_dates]
    within_period = [i for i in unique_dates if i >= comparison_date]
    final_dates = [datetime.strftime(a, '%d-%b-%Y') for a in within_period]

    return final_dates









