"""write vbscript to file"""

vbscript: str = """if WScript.Arguments.Count < 3 Then 
WScript.Echo "Please specify the source and the destination files. Usage: ExcelToCsv <xls/xlsx source file> <csv destination file> <worksheet number (starts at 1)>" 
Wscript.Quit 
End If

csv_format = 62 'xlCSVUTF8 '6

Set objFSO = CreateObject("Scripting.FileSystemObject")

src_file = objFSO.GetAbsolutePathName(Wscript.Arguments.Item(0))
dest_file = objFSO.GetAbsolutePathName(WScript.Arguments.Item(1))
worksheet_number = CInt(WScript.Arguments.Item(2))

Dim oExcel
Set oExcel = CreateObject("Excel.Application")

Dim oBook
Set oBook = oExcel.Workbooks.Open(src_file)
oBook.Worksheets(worksheet_number).Activate

oExcel.displayalerts=false  
oBook.SaveAs dest_file, csv_format
oExcel.displayalerts=true

oBook.Close False
oExcel.Quit
"""

def write_ExcelToCsv():
    """
    записывает vbs скрипт для конвертации экселя в csv
    """
    with open('ExcelToCsv.vbs', 'wb') as f:
        f.write(vbscript.encode('utf-8'))


if __name__ == '__main__':
    write_ExcelToCsv()
