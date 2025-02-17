from datetime import datetime, timedelta 
x = datetime.now()
y = x - timedelta(days=1)
z = x + timedelta(days=1)
print(y, y.strftime("%Y - %M - %D"))
print(x, x.strftime("%Y - %M - %D"))
print(z, z.strftime("%Y - %M - %D"))