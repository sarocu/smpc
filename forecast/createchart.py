from forecast import Forecast
import matplotlib.pyplot as plot
import matplotlib.dates as mdates
import seaborn
import pandas
import numpy

# Create the forecast object (default horizon = 24 hours):
weather = Forecast() # set horizon with Forecast(horizon=48)

# load weather data:
#weather.clean_tmy('../data/houston.csv') # this saves a 'cleaned' tmy file
weather.load_tmy('../data/atlanta_clean.csv')

# set the simulation time if necessary:
weather.simulation_time = '07/01/1900 01:00'

# Set up the VAR model by adding variables:
weather.add_predictor('Dry-bulb (C)').add_predictor('RHum (%)')

# Make a number of predictions and capture the predictions and the test data:
predictions, test = weather.auto_regressive(72, 50, trim_data=False)

# Extract a variable of interest (index values correspond to the order the variables were added):
db = predictions[weather.predictor_variables[0]]
rh = predictions[weather.predictor_variables[1]]

# ...and the test data:
dbtest = test[weather.predictor_variables[0]]
rhtest = test[weather.predictor_variables[1]]

# use seaborn to make a pretty plot:
f, (ax, ax2) = plot.subplots(2, 1)
pretty = seaborn.boxplot(data=db, ax=ax)
seaborn.tsplot(dbtest, ax=ax)

pretty2 = seaborn.boxplot(data=rh, ax=ax2)
seaborn.tsplot(rhtest, ax=ax2)
ax.set_title('50 Predictions of Dry-Bulb (C) and Relative Humidity (%) for Atlanta, GA on July 1st', fontsize=20)

pretty.set(xticklabels=numpy.arange(1, 25))
pretty2.set(xticklabels=numpy.arange(1, 25))
pretty.set_xlabel('Time (hours)', fontsize=14)
pretty.set_ylabel('Dry-Bulb (C)', fontsize=14)
pretty2.set_xlabel('Time (hours)', fontsize=14)
pretty2.set_ylabel('Relative Humidity (%)')
seaborn.set(font_scale=2)
seaborn.plt.show()