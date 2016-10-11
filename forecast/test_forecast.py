from forecast import Forecast
import matplotlib.pyplot as plot
import seaborn

weather = Forecast()

#weather.clean_tmy('../data/lafayette.CSV')
weather.load_tmy('../data/golden_clean.csv')
weather.simulation_time = '7/1/1900 08:00'

weather.add_predictor('Dry-bulb (C)').add_predictor('Dew-point (C)')

predictions, test = weather.auto_regressive(24, 50)
print('...predictions succeeded, now plotting...')

stuff = test[weather.predictor_variables[0]].T
# plot the first variable:
things = predictions[weather.predictor_variables[0]]
f, ax = plot.subplots(1,1)
p = seaborn.boxplot(data=things, ax=ax)
seaborn.tsplot(stuff, ax=ax)
for item in p.get_xticklabels():
    item.set_rotation(25)
seaborn.plt.show()
weather.persist()
