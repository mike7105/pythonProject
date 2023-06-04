"""Test to load Excel to Pandas"""
import pandas as pd
from subprocess import call
import os
import re
import savReaderWriter
import pyreadstat

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
    # writeVBscript.write_ExcelToCsv()
    csvfile = file.replace(".xlsx", ".csv")
    # call(['cscript.exe', 'ExcelToCsv.vbs', file, csvfile, "Лист1"])

    res: pd.DataFrame = pd.read_csv(csvfile, engine="pyarrow")

    # for f in ['ExcelToCsv.vbs', csvfile]:
    #     if os.path.isfile(f):
    #         os.remove(f)
    varLabs = {}
    varTypes = {}
    varFormats = {}
    what: re.Pattern = re.compile(r'[^a-zA-Zа-яА-Я_0-9№]')
    for c in res.columns:
        n: str = what.sub('', c)[:32]
        if c != n:
            res.rename(columns={c: n}, inplace=True)
        varLabs[n] = c

        if str(res[n].dtype) == "object":
            res[n] = res[n].astype(str).fillna("").str.replace("nan", "").str.strip()
            varTypes[n] = 1024
            varFormats[n] = "A1024"
        else:
            varTypes[n] = 0
            varFormats[n] = "F8.2"

    # saveSPSS("baseSRW.zsav", res, varLabs, varTypes, varFormats)
    saveSPSS2("basePRS.zsav", res, varLabs, varTypes, varFormats)
    return res

def saveSPSS(fname: str, dwm: pd.DataFrame, varLabs: dict, varTypes: dict, varFormats: dict):
    """
    Сохраняет SPSS из датафрейма savReaderWriter
    :param str fname: файл, в который сохраняем
    :param dict varLabs: varLabels
    :param dict varTypes: varTypes
    :param dict varFormats: formats
    :param pd.DataFrame dwm: датакласс с фреймом и метаданными
    """
    colsSave: list = list(dwm.columns)
    records: list = list(dwm.values)
    # https://pythonhosted.org/savReaderWriter/generated_api_documentation.html?highlight=savwriter#savReaderWriter.SavWriter
    with savReaderWriter.SavWriter(fname.encode('utf-8'), varNames=colsSave, varTypes=varTypes,
                                   valueLabels={}, varLabels=varLabs,
                                   formats=varFormats, ioUtf8=True) as writer:
        for record in records:
            writer.writerow(record)


def saveSPSS2(fname: str, dwm: pd.DataFrame, varLabs: dict, varTypes: dict, varFormats: dict):
    """
    Сохраняет SPSS из датафрейма pyreadstat
    :param str fname: файл, в который сохраняем
    :param dict varLabs: varLabels
    :param dict varTypes: varTypes
    :param dict varFormats: formats
    :param pd.DataFrame dwm: датакласс с фреймом и метаданными
    """

    # https://ofajardo.github.io/pyreadstat_documentation/_build/html/index.html#pyreadstat.pyreadstat.write_sav
    pyreadstat.write_sav(df=dwm, dst_path=fname.encode('utf-8'), compress=True, column_labels=varLabs,
                         variable_value_labels={}, missing_ranges={}, variable_display_width={},
                         variable_measure={}, variable_format=varFormats)
