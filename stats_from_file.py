import json

# Fields
F_NUM = 'num'
F_DATE = 'date'
F_DURATION = 'duration'
F_DISTANCE = 'distance'
F_PRICE = 'price'


def get_value(data, begin_str, end_str):
    index = data.find(begin_str) + len(begin_str)
    end_index = data.find(end_str, index)
    return data[index:end_index]


def get_ride_info(num, info):
    ride = {F_NUM: num}

    date = 'date h_mb10">'
    date_end = '<'
    date_value = get_value(info, date, date_end)
    ride[F_DATE] = date_value

    duration = '"routes-list__time">'
    duration_end = '<'
    duration_value = get_value(info, duration, duration_end)
    ride[F_DURATION] = int(duration_value[2:-8])

    distance = '"routes-list__distance">'
    distance_end = '<'
    distance_value = get_value(info, distance, distance_end)
    ride[F_DISTANCE] = float(distance_value[:-5])

    price = '"routes-list__price">'
    price_end = '<'
    price_value = get_value(info, price, price_end)
    price_value = price_value.strip()[:-4]
    if len(price_value) != 14:
        ride[F_PRICE] = int(price_value)
    else:
        ride[F_PRICE] = 0

    print(ride)
    return ride


data = ''
with open('data.txt', 'r') as f:
    data = f.read()

items = []
item_code_begin = '<li class="history-list__item" data-id="0">'
item_end = '===END==='

item_index = 0
while (item_index >= 0):
    item_index = data.find(item_code_begin, item_index + 1)
    if item_index > 0:
        item_end_index = data.find(item_end, item_index)
        item = data[item_index:item_end_index]
        items.append(item)

ride = {'num': 0, 'date': '', 'duration': '', 'distance': '', 'price': ''}
rides = []

for index, item in enumerate(items):
    rides.append(get_ride_info(index, item))

print(rides)

with open('filtered_data.txt', 'w') as f:
    json.dump(rides, f)
