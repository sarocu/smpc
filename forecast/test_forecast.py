from forecast import Forecast
import matplotlib.pyplot as plot
import seaborn
import pandas
import numpy

atlanta = Forecast()

#weather.clean_tmy('../data/lafayette.CSV')
atlanta.load_tmy('../data/atlanta_clean.csv')
atlanta.simulation_time = '07/01/1900 08:00'

#weather.add_predictor('GHI (W/m^2)').add_predictor('DNI (W/m^2)')
atlanta.add_predictor('Dry-bulb (C)').add_predictor('Dew-point (C)')

# now let's look at colorado:
golden = Forecast()
golden.load_tmy('../data/golden_clean.csv')
golden.simulation_time = '07/01/1900 08:00'

#weather.add_predictor('GHI (W/m^2)').add_predictor('DNI (W/m^2)')
golden.add_predictor('Dry-bulb (C)').add_predictor('Dew-point (C)')

"""
# Grab predictions for 10, 50 and 100 scenarios:
predictions, test = weather.auto_regressive(24, 10)
print('...predictions succeeded, now plotting...')

stuff = test[weather.predictor_variables[0]].T
junk = test[weather.predictor_variables[1]].T

n10DB = predictions[weather.predictor_variables[0]]
n10DP = predictions[weather.predictor_variables[1]]

predictions, test = weather.auto_regressive(24, 50)

n50DB = predictions[weather.predictor_variables[0]]
n50DP = predictions[weather.predictor_variables[1]]

predictions, test = weather.auto_regressive(24, 100)

n100DB = predictions[weather.predictor_variables[0]]
n100DP = predictions[weather.predictor_variables[1]]

hour = '1900-07-01 15:00:00'
n10 = n10DB[hour]
n10.rename('n10', inplace=True)
n50 = n50DB[hour]
n50.rename('n50', inplace=True)
n100 = n100DB[hour]
n100.rename('n100', inplace=True)

data = pandas.concat([n10, n50, n100], axis=1)

p = seaborn.boxplot(data=data)
p.set(title='Dry bulb temperature ranges at 15:00 on July 1st', xlabel='Number of scenarios generated', ylabel='Dry Bulb (C)')

seaborn.plt.show()

"""
predictions, test = atlanta.auto_regressive(48, 50, trim_data=False)
db = predictions[atlanta.predictor_variables[0]]
testAtl = test[atlanta.predictor_variables[0]]

predictions, test = golden.auto_regressive(48, 50, trim_data=False)
goldenDB = predictions[golden.predictor_variables[0]]
testGold = test[golden.predictor_variables[0]]
print('...predictions succeeded, now plotting...')

f, (ax, ax2) = plot.subplots(2,1)
p = seaborn.boxplot(data=goldenDB, ax=ax)
p2 = seaborn.boxplot(data=db, ax=ax2)
seaborn.tsplot(testGold, ax=ax)
seaborn.tsplot(testAtl, ax=ax2)
#ax.set_title('GLobal Horizontal Irradiation (W/m^2)')
ax.set_title('Dry-Bulb (C) for Golden, CO')
ax.xaxis.set_ticklabels([])
#ax2.set_title('Direct Normal Irradiation (W/m^2)')
ax2.set_title('Dry-Bulb (C) for Atlanta, GA')
for item in p.get_xticklabels():
    item.set_rotation(25)
for item in p2.get_xticklabels():
    item.set_rotation(25)	
seaborn.plt.show()

# save predictions to csv:
#drybulb = pandas.DataFrame(things)
#dewpoint = pandas.DataFrame(junk)
#drybulb.to_csv("goldenDB.csv")
#dewpoint.to_csv("goldenDP")	