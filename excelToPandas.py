"""Test to load Excel to Pandas"""
import pandas as pd
from subprocess import call
import os
import writeVBscript

def read_excel(file: str) -> pd.DataFrame:
    """
    read Excel with standard Pandas method read_excel
    :param str file: path to xlsx file
    :return pd.DataFrame: Dataframe from Excel
    """
    return pd.read_excel(file, sheet_name=0)

def read_excle_csv(file: str) -> pd.DataFrame:
    """
    convert Excel to csv and then read_csv
    :param str file: path to xlsx file
    :return pd.DataFrame: Dataframe from Excel
    """
    writeVBscript.write_ExcelToCsv()
    csvfile = file.replace(".xlsx", ".csv")
    call(['cscript.exe', 'ExcelToCsv.vbs', file, csvfile, "1"])

    res: pd.DataFrame = pd.read_csv(csvfile)

    for f in ['ExcelToCsv.vbs', csvfile]:
        if os.path.isfile(f):
            os.remove(f)

    return res
