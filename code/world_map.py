
import matplotlib.pyplot as plt
import geopandas as geopd

data = {
'India' : (0.1, 0.4), 
'Europe' : (0.15, 0.2), 
'USA' : (0.56, 0.83), 
'Bahamas' : (0, 0.9), 
'Japan' : (0.3, 0.4)
}

locations = {'India' : (78, 21), 'USA' : (-100, 40), 'Europe' : (5, 48), 'Bahamas' : (-77, 21), 'Japan' : (138, 37)}


circleLocation = plt.Circle((-180, -25), 0.5, color='r')
circleDisaster = plt.Circle((-180, -33), 5, color='r', alpha = 0.3)
circleClimate = plt.Circle((-180, -45), 5, color='b', alpha = 0.3)

fig, ax = plt.subplots()

ax = fig.gca()

world = geopd.read_file(geopd.datasets.get_path('naturalearth_lowres'))


world.plot(ax=ax, color = 'white', edgecolor = 'black', linewidth = 0.3)

# circles = {'India' : circleIndia, 'USA' : circleUSA, 'Europe' : circleEurope, 'Bahamas' : circleBahamas, 'Japan' : circleJapan}

for location in locations:
    circle = plt.Circle(locations[location], 0.2, color='r')
    ax.add_patch(circle)
    circle_disaster = plt.Circle((locations[location][0], locations[location][1]), data[location][1] * 15, color='r', alpha = 0.3)
    ax.add_patch(circle_disaster)
    circle_climate = plt.Circle((locations[location][0], locations[location][1]), data[location][0] * 25, color='b', alpha = 0.3)
    ax.add_patch(circle_climate)

ax.add_patch(circleLocation)
ax.add_patch(circleClimate)
ax.add_patch(circleDisaster)

plt.text(-170, -27.5, "Disaster location", size = 5)
plt.text(-170, -35.5, "Disaster intensity", size = 5)
plt.text(-170, -47.5, "Climate talk intensity", size = 5)
plt.show()