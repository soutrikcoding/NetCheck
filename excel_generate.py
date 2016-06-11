import xlwt
from datetime import datetime

style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',num_format_str='#,##0.00')
	
wb = xlwt.Workbook()
ws = wb.add_sheet('Log')

def generate_excel() :
	
	ws.write(0, 4, "Event ID", style0)
	ws.write(0, 5, "IP Address", style0)
	ws.write(0, 6, "Location", style0)
	ws.write(0, 7, "Checking Time", style0)
	wb.save('Link_Down.xls')
	
def write_to_excel(rownum, ip_address, location) :

	ws.write(rownum, 4, rownum, style0)
	ws.write(rownum, 5, ip_address, style0)
	ws.write(rownum, 6, location, style0)
	ws.write(rownum, 7, str(datetime.now()), style0)
	wb.save('Link_Down.xls')
