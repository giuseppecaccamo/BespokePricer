
import pandas as pd
import datetime as dtm
#import os


def writing_dictionary_to_excel(filepath, dicts, sheetnames):

    writer = pd.ExcelWriter(filepath,'xlsxwriter')


    for i, value in enumerate(dicts):

        dicts[i].to_excel(writer, sheet_name=sheetnames[i], encoding='utf-8')

    writer.save()

def saving_figure_to_folder(report, path, namefig):


    plot= report.plot(kind='bar', figsize=(10, 9), title='bespoke pricers usage frequency', grid=1)
    plot.set_xticklabels(plot.get_xticklabels(), rotation=0)
    plot.axis('tight')
    fig= plot.get_figure()
    fig.savefig(path+namefig+'.jpeg')
    fig_name = namefig+'.jpeg'
    return fig_name
