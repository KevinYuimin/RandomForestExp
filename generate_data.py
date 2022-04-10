import csv
import random

random.seed(1337)

# all in range [0,100]

TOLERABLE = {
    "CO2": [0, 40],
    "AQI": [0, 75],
    "PM2.5": [0, 15], # [0, 15 , 35]
    "PM10": [0, 50],
    "Rain": [0, 30], # [0 means no rain, 30 means small rain, 100 heavy rain],
    "Smoke": [0, 20], 
}

NUM_DATA = 1000

headers = list(TOLERABLE.keys())
data = []
pos_ctr = 0
neg_ctr = 0
while pos_ctr<NUM_DATA or neg_ctr<NUM_DATA:
    print(pos_ctr, neg_ctr)
    data_point = []
    is_safe = True
    for k in headers:
        val = random.randint(0, 100)
        up = TOLERABLE[k][1]
        lo = TOLERABLE[k][0]
        if val > up or val < lo:
            is_safe = False
        data_point.append(val)
    data_point.append(0 if is_safe else 1)
    if is_safe and neg_ctr < NUM_DATA:
        data.append(data_point)
        neg_ctr+=1
    elif not is_safe and pos_ctr< NUM_DATA:
        pos_ctr+=1
        data.append(data_point)

headers.append("label")
import csv

# open the file in the write mode
with open('data.csv', 'w') as f:
    # create the csv writer
    writer = csv.writer(f)
    writer.writerow(headers)
    for pt in data:
        writer.writerow(pt)


