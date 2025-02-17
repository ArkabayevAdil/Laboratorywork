from datetime import datetime
def time(date1, date2):
    x = datetime.strptime(date1, "%Y-%d-%m %H:%M:%S")
    y = datetime.strptime(date2, "%Y-%d-%m %H:%M:%S")
    z = y - x
    print(z.total_seconds())

"""x = int(input("first date:"))
y = int(input("second date:"))"""

x = '2020-12-12 12:12:12'
y = '2020-12-12 14:11:11'
time(x,y)