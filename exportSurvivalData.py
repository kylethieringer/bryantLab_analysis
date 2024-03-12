"""
code to export raw data from survival assays to a form that can be copied into prism

author: kyle thieringer
date: 2024-03-11

"""

import os
import pandas as pd
import numpy as np
from tkinter import Tk, filedialog

# define 3 temperatures
# if you want more, hopefully you can see how these are used and can add more as needed below
lowTemp = 23
midTemp = 30
highTemp = 37


def load_data(filepath):
    """ load data using pandas 
    Args:
        filepath: (str) path to excel file containing survival data
    
    Returns:
        datatable: pandas dataframe of the raw data
    """
    
    datatable = pd.read_excel(filepath)

    return datatable


def filter_datatable(datatable, wormSex=None):
    """ get rid of unnecessary columns in the excel file
    Args:
        datatable: pandas dataframe of raw data
        wormSex: (str) which sex to continue for analysis. None ignores sex column
    Returns:
        lowdata: dataframe containing only low temp data
        middata: dataframe containing only middle temp data
        highdata: dataframe containing only high temp data
    """
    # extract column names
    columnNames = []
    for cn in datatable.keys():
        if 'eggs' in cn:
            continue
        columnNames.append(cn)

    if wormSex is not None:
        sexIDX = datatable.sex == wormSex
    else:
        sexIDX = np.ones(len(datatable)).astype(bool)

    if 'exclude' in datatable:
        keepIDX = datatable.exclude != 1
    else:
        keepIDX = np.ones(len(datatable)).astype(bool)

    # separate temperatures
    lowtemp = datatable.temp == lowTemp
    midtemp = datatable.temp == midTemp
    hightemp = datatable.temp == highTemp

    lowdata = datatable[(sexIDX & keepIDX & lowtemp)][columnNames]
    middata = datatable[(sexIDX & keepIDX & midtemp)][columnNames]
    highdata = datatable[(sexIDX & keepIDX & hightemp)][columnNames]

    return lowdata, middata, highdata


def convert_datatable(lowdata, middata, highdata):
    """ convert the excel data format to prism plotting format
    Args:
        lowdata: dataframe containing only low temp data
        middata: dataframe containing only middle temp data
        highdata: dataframe containing only high temp data
    Returns:
        newdatatable: dataframe containing all data in format to copy to prism
    """
    dayNames = []
    for cn in lowdata.keys():
        if cn.startswith('Day'):
            dayNames.append(cn)
    
    newdatatable = pd.DataFrame(columns=['time', str(lowTemp), str(midTemp), str(highTemp)])
    for day in dayNames:
        for i in range(int(lowdata[day].sum())):
            newdatatable.loc[len(newdatatable)] = [day[-1], 1, '', '']
        for i in range(int(middata[day].sum())):
            newdatatable.loc[len(newdatatable)] = [day[-1], '', 1, '']
        for i in range(int(highdata[day].sum())):
            newdatatable.loc[len(newdatatable)] = [day[-1], '', '', 1]

    return newdatatable


def save_newData(newdatatable, savepath):
    """ save data 
    Args:
        newdatatable: dataframe with prism format data
        savepath: (str) path to save file

    """
    newdatatable.to_csv(savepath)


def select_file():
    """ opens window to select which file to convert
    Returns:
        file_path: path to file 
    """
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    file_path = filedialog.askopenfilename(title="Select a file")  # show an "Open" dialog box and return the path to the selected file
    return file_path


def filter_sex():
    """ asks user input if we should filter out by sex of worms
    Returns:
        sf: (str) M or F or None
    """
    sexFilter = input("which sex for analysis? [ M / F / or empty to ignore]: ")
    if not len(sexFilter):
        sf = None
    else:
        sf = sexFilter
    return sf


def get_savepath(fp):
    """ asks user input for filename to save to. default location is same folder as excel file
    Args:
        fp: (str) filepath to raw data
    Returns:
        sp: (str) filepath where to save 
    
    """
    sp_filename = input("what should we call the new file? [leave blank for default]: ")

    if not len(sp_filename):
        sp = os.path.join(os.path.dirname(fp), 'exportedSurvival_forPrism.csv')
    else:
        if not sp_filename.endswith('.csv'):
            sp_filename = sp_filename+'.csv'
        sp = os.path.join(os.path.dirname(fp), sp_filename)
    return sp


def main():

    fp = select_file()
    print('\n\nwill load data from : ', fp)

    sp = get_savepath(fp)
    print('\n\nwill save new file to: ', sp)

    sf = filter_sex()

    datatable = load_data(fp)

    lowdata, middata, highdata = filter_datatable(datatable, wormSex=sf)

    newdatatable = convert_datatable(lowdata, middata, highdata)

    save_newData(newdatatable, sp)
    print("\n\nnew file saved!! all done!!")


if __name__ == "__main__":

    main()
   




    
