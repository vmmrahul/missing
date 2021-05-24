import datetime

d = "01/05/2021"
datetimeNew = datetime.datetime.strptime(d, '%d/%m/%Y')
datetimeNew = datetime.datetime.strptime(d, '%d/%m/%Y')
# datetimeNew = datetimeNew.strftime('%m-%d-%Y')
print(datetimeNew.date())


name = "demo.png"
print(name.split("."))
