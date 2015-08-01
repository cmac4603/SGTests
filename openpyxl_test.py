from datetime import date
from openpyxl import load_workbook

today = date.today()

wb = load_workbook('CSV Test Sheet.xlsx')

ws2 = wb.get_sheet_by_name("Left")
ws3 = wb.get_sheet_by_name("Right")

print(ws2)
print(ws3)