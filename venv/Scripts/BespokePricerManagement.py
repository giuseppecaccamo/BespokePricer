import os
import numpy as np
import re
import pandas as pd
import io
import datetime as dtm
import matplotlib.pyplot as plt
from BespokePricerDictionaries import (populate_dictionary, sort_dict_by_date, add_column_to_dict)
from BespokePricerCurrentPricersAnalysis import number_of_timeoccurrencies, dates_within_period
from UtilityFunctions import writing_dictionary_to_excel
from UtilityFunctions import saving_figure_to_folder
from ReportCreation import report_creation



directory = 'S:\Valuations\Log'
os.chdir(directory)


file = []
old=[]
current=[]
other_path=[]
pricer=[]
current_dict = {'last user':[],'path':[],'last time opened':[],'Model identity':[], 'name':[], 'frequency':[]}
current_old_folder_dict = {'last user':[],'path':[],'last time opened':[],'Model identity':[],'name':[], 'frequency':[]}
other_path_dict = {'last user':[],'path':[],'last time opened':[],'Model identity':[],'name':[], 'frequency':[]}
old_dict = {'last user':[],'path':[],'last time opened':[],'Model identity':[],'name':[], 'frequency':[]}
pricer_dict = {'last user':[],'path':[],'last time opened':[],'Model identity':[],'name':[], 'frequency':[]}
num_current = 0
number_of_occurrencies = []
dates = []


for i, filenames in enumerate(os.listdir(directory)):

    file.append([])

    if '.txt' in filenames:

        file_object=io.open(directory+"/"+filenames ,mode='r')
        filecontents = file_object.readlines()
        file[i].append(filecontents[0])

        if len(filecontents)>1:#if they are not old versions
            file[i].append(filecontents[-1])


            if 'Models\Client Valuation' in file[i][1]:#In the current folder

                if 'Archive' not in file[i][1] and 'Old' not in file[i][1] and 'OLD' not in file[i][1] and 'Obsolete' not in file[i][1]: #in use
#                    if 'LGIM_MPlus_IndexRol' in file[i][1]:

#                        print 'ok'

                    current.append(filecontents)
                    [n, occur_dates] = number_of_timeoccurrencies(current[num_current])
                    number_of_occurrencies.append(n)
                    dates_within=dates_within_period(occur_dates, 92)
                    dates.append(dates_within)
                    current_dict = populate_dictionary(current_dict, filecontents[-1])
                    num_current = num_current +1

                else:
                    current_old_folder_dict = populate_dictionary(current_old_folder_dict, filecontents[-1])

            else:

                if 'Models\Generic Pricers' in file[i][1]:

                    pricer.append(filecontents)
                    pricer_dict = populate_dictionary(pricer_dict, filecontents[-1])

                else:
                    other_path.append(filecontents)
                    other_path_dict = populate_dictionary(other_path_dict, filecontents[-1])

        else:
            file[i].append('file opened only once')
            old.append(filecontents[0])
            old_dict = populate_dictionary(old_dict , filecontents[0])
    else:
        file[i].append(filenames)

#dataframe creation and sorting procedure


current_dict = pd.DataFrame(current_dict)
add_column_to_dict(current_dict, number_of_occurrencies, 'times opened')
add_column_to_dict(current_dict, dates, 'dates opened')
current_dict = sort_dict_by_date(current_dict)
report = current_dict['frequency'].str.lower().value_counts()

current_old_folder_dict = pd.DataFrame(current_old_folder_dict)
current_old_folder_dict = sort_dict_by_date(current_old_folder_dict)

other_path_dict = pd.DataFrame(other_path_dict)
other_path_dict = sort_dict_by_date(other_path_dict)

old_dict = pd.DataFrame(old_dict)
old_dict = sort_dict_by_date(old_dict)

pricer_dict = pd.DataFrame(pricer_dict)
pricer_dict = sort_dict_by_date(pricer_dict)

# creation of an excel file

today =dtm.datetime.now()
filepath = unicode('S:\Valuations\Rates\Rates_Projects\BespokePricer\Bespoke_files_info'+ str(today)[:10]+'.xlsx', encoding='utf-8')
dicts = [report, current_dict, current_old_folder_dict, other_path_dict, old_dict, pricer_dict]
sheetnames =['report','currently used', 'old folders', 'other path', 'Old versions', 'Generic pricers']

writing_dictionary_to_excel(filepath, dicts, sheetnames)
namefig = '\histogram' + str(today)[:10]
saving_figure_to_folder(report,'S:\Valuations\Rates\Rates_Projects\BespokePricer', namefig)

report_creation('S:\Valuations\Rates\Rates_Projects\BespokePricer', 'FinalReport'+str(today)[:10]+'.pdf', 'histogram' + str(today)[:10]+'.jpeg', report, current_dict)


