import json
import pygal

# Fields
F_NUM = 'num'
F_DATE = 'date'
F_DURATION = 'duration'
F_DISTANCE = 'distance'
F_PRICE = 'price'

rides = []

with open('filtered_data.txt', 'r') as f:
    rides = json.load(f)

# Remove rides with duration less than 5 mins
print('All rides: {}'.format(len(rides)))

rides_5 = rides
for ride in rides_5:
    if ride[F_DURATION] < 5:
        rides_5.remove(ride)
print('Rides more than 5 mins: {}'.format(len(rides_5)))

# Total price
stat_prices = []
for ride in rides:
    stat_prices.append(ride[F_PRICE])
print('Rides total price: {}'.format(sum(stat_prices)))

# Distance
stat_distance = []
for ride in rides:
    stat_distance.append(ride[F_DISTANCE])
print('Rides distance: {0:0.2f}'.format(sum(stat_distance)))

# Duration
stat_duration = []
for ride in rides:
    stat_duration.append(ride[F_DURATION])
duration = sum(stat_duration)
h = int(duration / 60)
m = duration - h * 60
print('Rides duration: {} h {} m'.format(h, m))

# Free rides
free_rides = 0
for ride in rides:
    if ride[F_PRICE] == 0:
        free_rides += 1
print('Free rides: {}'.format(free_rides))

# Ride duration by date
dates = []
durs = []
distances = []
for ride in rides:
    if ride[F_DATE] in dates:
        durs[len(durs) - 1] += ride[F_DURATION]
        distances[len(distances) - 1] += ride[F_DISTANCE]
    else:
        dates.append(ride[F_DATE])
        durs.append(ride[F_DURATION])
        distances.append(ride[F_DISTANCE])

# Average rides (more than 5 min)
rides_5_dist = []
for ride in rides_5:
    rides_5_dist.append(ride[F_DISTANCE])
rides_average = sum(rides_5_dist) / len(rides_5_dist)
print('Average ride duration: {}'.format(int(rides_average)))


'''line_chart = pygal.Bar()
line_chart.title = 'Ride duration by date'
line_chart.x_labels = dates
line_chart.add('', distances)
line_chart.render_to_file('stats.svg')'''
