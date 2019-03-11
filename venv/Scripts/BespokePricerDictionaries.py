#dictionaries for the bespoke pricer Management here
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtm
from pandas.tseries.offsets import BDay, BMonthEnd

import datetime

def populate_dictionary(dictionary, string, n = None, dates = None):


    temp = string.split(';')
    file_name = temp[1].split('\\')[-1]
    dictionary['last user'].append(temp[0])
    dictionary['path'].append(temp[1].replace(file_name,''))
    dictionary['last time opened'].append(temp[3])
    dictionary['name'].append(file_name)

    if len(temp)> 5:
        temp[5]=temp[5].replace('Model identity:', '')

        if 'frequency' in temp[5]:

            new_tuple = temp[5].partition('frequency:')
            dictionary['frequency'].append(new_tuple[2])
            temp[5]=temp[5].replace('frequency:'+new_tuple[2],'')

        else:

            dictionary['frequency'].append('not provided')

        dictionary['Model identity'].append(temp[5])

    else:

        dictionary['Model identity'].append('Model Identity not provided')
        dictionary['frequency'].append('not provided')



    return dictionary


def sort_dict_by_date(dict):

    dict['last time opened']=pd.to_datetime(dict['last time opened'])
    temp = dict.sort_values(by='last time opened',ascending='False')

    return temp

def add_column_to_dict(dict, column, column_name):

    temp = pd.Series(column)
    dict[column_name] = temp.values

    return

def associate_client_to_pricer_table(dict, path):

    today = dtm.datetime.now()
    os.chdir(path)

    short_path = [w.replace('S:\\Valuations\\Models\\Client Valuation\\','') for  w in dict['path']]
    short_path = [w.replace('\\\\markit.partners\\dfs\\UK\\Shared\\Valuations\\Models\\Client Valuation\\', '') for w in short_path]
    short_path = np.array(short_path)

    pricers_name = [ name for  name in dict['name']]
    pricers_name = np.array(pricers_name)

    table = np.hstack([np.expand_dims(pricers_name,axis=1), np.expand_dims(short_path,axis=1)])

    return table

def report_frame_creation(dataframe, path):

    today = dtm.datetime.now()
    os.chdir(path)
    data = dataframe.to_frame()
    for i, string in enumerate(data.axes[0]):
        data.axes[0].values[i] = string.rstrip()
    fig, axs = plt.subplots(1, 1)
    axs.axis('tight')
    axs.axis('off')
    axs.table(cellText=np.hstack([data.axes[0].values.reshape(data.values.shape), data.values]),
              colLabels=['frequency', 'number of pricers'], cellLoc='center', loc='center')
    axs.set_title('situation as of '+str(today)[:10])
    fig.savefig('frequency report' + str(today)[:10]+'.jpeg')

    name_today = 'frequency report' + str(today)[:10]+'.jpeg'
    name_lastBusiness_MonthEnd = 'frequency report' + str(find_last_BD_MonthEnd(today))[:10] + '.jpeg'
    a = check_file_presence(name_lastBusiness_MonthEnd)

    if a==0:
        while a == 0:
            t = subtract_one_month(today)
            name_lastBusiness_MonthEnd = 'frequency report' + str(find_last_BD_MonthEnd(t))[:10] + '.jpeg'
            a = check_file_presence(name_lastBusiness_MonthEnd)


    return name_today, name_lastBusiness_MonthEnd


def find_last_BD_MonthEnd(date):

    offset = BMonthEnd()

    return offset.rollback(date)


def check_file_presence(fileName):

    directory = 'S:\Valuations\Rates\Rates_Projects\BespokePricer'

    check = []
    for i, filenames in enumerate(os.listdir(directory)):


        if fileName in filenames:

            check.append(1)

        else:

            check.append(0)

    return sum(check)


def subtract_one_month(t):
    one_day = datetime.timedelta(days=1)
    one_month_earlier = t - one_day
    while one_month_earlier.month == t.month or one_month_earlier.day > t.day:
        one_month_earlier -= one_day
    return one_month_earlier
