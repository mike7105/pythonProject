"""Dot to Enter"""
import excelToPandas
import timeit
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name: str):
    """
    Just example to print name
    :param str name: any string name
    """
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # pFile = "base.xlsx"
    # print("read_excel:")
    # # print(excelToPandas.read_excel(pFile).shape)
    # print(timeit.timeit(setup="import excelToPandas; pFile = 'base.xlsx'", stmt="excelToPandas.read_excel(pFile)",
    #                     number=1))
    print()
    print("read_excle_csv:")
    # print(excelToPandas.read_excle_csv(pFile).shape)
    print(timeit.timeit(setup="import excelToPandas; pFile = 'base.xlsx'", stmt="excelToPandas.read_excle_csv(pFile)",
                        number=1))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
