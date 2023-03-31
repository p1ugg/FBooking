import csv
from datetime import datetime, date, timedelta
from pprint import pprint
dict_docs = dict()
with open('data/doc_list.csv', 'r', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        b = row
        dates = b[2].split(',')
        now = datetime.now()
        sp = list()
        for i in range(0, 8):
            a = now + timedelta(days=i)
            sp.append(a.strftime("%d/%m/%y"))

        new_sp = list()
        for i in range(len(dates)):
            a = dates[i]
            if 'None' in a:
                sp_time = 'Не работает'
            else:
                a = list(map(int, str(a.split()[1]).replace('00', '').replace(':', '').split('-')))
                start = a[0]
                endd = a[1]
                sp_time = list()
                for i in range(start, endd):
                    sp_time.append(f'{i}:00-{i + 1}:00')
            new_sp.append(sp_time)

        Dates = dict()
        for i in sp:
            datte = list(map(int, i.split('/')))
            d = date(datte[2], datte[1], datte[0])
            dd = date.weekday(d)
            Dates[i] = new_sp[dd]

        dict_docs[row[0]] = Dates
# pprint(dict_docs)
for i in dict_docs.items():
    n = i[1]
    # print(i[0])
    # for j in n.items():
        # print(f'{j[0]} - {j[1]}')
