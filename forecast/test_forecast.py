from forecast import Forecast
import matplotlib.pyplot as plot
import seaborn

weather = Forecast()

#weather.clean_tmy('../data/lafayette.CSV')
weather.load_tmy('../data/golden_clean.csv')
weather.simulation_time = '7/1/1900 08:00'

weather.add_predictor('GHI (W/m^2)').add_predictor('DNI (W/m^2)')

predictions, test = weather.auto_regressive(24, 10)
print('...predictions succeeded, now plotting...')

stuff = test[weather.predictor_variables[0]].T
junk = test[weather.predictor_variables[1]].T

things = predictions[weather.predictor_variables[0]]
morethings = predictions[weather.predictor_variables[1]]
f, (ax, ax2) = plot.subplots(2,1)
p = seaborn.boxplot(data=things, ax=ax)
p2 = seaborn.boxplot(data=morethings, ax=ax2)
seaborn.tsplot(stuff, ax=ax)
seaborn.tsplot(junk, ax=ax2)
ax.set_title('GLobal Horizontal Irradiation (W/m^2)')
ax.xaxis.set_ticklabels([])
ax2.set_title('Direct Normal Irradiation (W/m^2)')
for item in p.get_xticklabels():
    item.set_rotation(25)
for item in p2.get_xticklabels():
    item.set_rotation(25)	
seaborn.plt.show()
weather.persist()
