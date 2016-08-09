import pickle

from pyswarm import pso
import pandas
import numpy

class Superplus:
    """superplus implements a particle swarm optimization for determining setpoint temperatures

    Several instance variables are created in order to manage the simulation:
    self.model -- the meta model used for determining the cost of the candidate setpoints
    self.simtime -- the 'current' time for passing on to the meta model
    self.horizon -- the optimization horizon, default = 24 hours
    self.maxlags -- max lags to pass to the VAR fit
    self.currentWeather -- a container for weather vectors
    """
    def __init__(self, metaModel):
        self.model = metaModel
        self.simulation_time = '7/1/1900 01:00' # in the future the node wrapper should track this...
        self.scenarios = 100 # number of weather scenarios to generate
        self.horizon = 24
        self.maxlags = 12
        self.weather = []
        self.determine = None
        self.upperbound = 50 # C
        self.lowerbound = 0 # C

    def persist(self, fileName='superplus.p'):
        pickle.dump(self, open(fileName, 'wb'))


    """
    Sets the weather generator to produce possible 24 hour weather vectors

    Params:
    forecast -- an initialized forecast object
    """
    def set_weather_generator(self, forecast):
        self.generator = forecast
        return self


    """
    Draws a number of possible weather vectors (from the start of self.simtime to
    self.simtime + horizon) for use in the deterministic and stochastic methods

    Params:
    number_of_samples -- the total number of samples to be generated through the
    forecast object self.generator
    """
    def create_weather_vectors(self, number_of_samples=100):
        try:
            self.generator.set_simtime(self.simulation_time)
            return self.generator.auto_regressive(self.maxlags, number_of_samples)
        except:
            print('weather generator not set!')


    """
    Sets the lower and upper setpoint temperature bounds
    """
    def set_constraints(self, upperbound, lowerbound):
        self.upperbound = upperbound
        self.lowerbound = lowerbound

    """
    This method makes an optimization assuming that the weather prediction is perfect,
    that is it uses a single weather realization and optimizes the setpoint strategy
    accordingly.
    """
    def deterministic(self):
        # create upper and lower bound matrices:
        setpointList = self.model.setpoints
        upperbounds = numpy.zeros((self.horizon, len(setpointList)))
        upperbounds.fill(self.upperbound)
        lowerbounds = numpy.zeros((self.horizon, len(setpointList)))
        lowerbounds.fill(self.lowerbound)

        def cost(setpoints):
            # get weather vector:
            self.determine = self.create_weather_vectors(1)[0]

            # create a dataframe using the weather vector and setpoint matrix:
            weather = pandas.DataFrame(self.determine, columns=self.generator.predictor_variables)
            sp = pandas.DataFrame(setpoints, columns=setpointList)
            data = pandas.concat([weather, sp], axis=1)
            prediction = self.model.predict(data)
            total_cost = numpy.sum(prediction)
            return total_cost


        # run the optimiztion:
        return pso(cost, lowerbounds, upperbounds)

    """
    This method draws a number of sample weather predictions from the generator
    """
    def stochastic(self, setpoints):
        self.weather = create_weather_vectors(self.scenarios)
