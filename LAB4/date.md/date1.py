from datetime import datetime, timedelta
x = datetime.now()
y = x - timedelta(days=5)
print(x, x.strftime("%Y - %m - %d"))
print(y, y.strftime("%Y - %M - %D"))
