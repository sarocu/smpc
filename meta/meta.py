import pickle
from datetime import datetime
import numpy as np

from scipy import stats as stats
from sklearn.cross_validation import cross_val_score
from sklearn.svm import SVR
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import BayesianRidge
import pandas


class MetaModel:
    """Fit a statistical model to data produced by a building energy model

    Intended to simplify highly non-linear building energy simulation models
    by fitting one of several statistical models to hourly simulation data.
    Contains methods for fitting models and comparing the goodness of fit via
    generalized cross validation.

    Relies on pandas for data processing and sklearn for modeling.
    """
    def __init__(self):
        """Constructor method for class metaModel

        Creates the following instance variables:
        self.response -- the dependent variable
        self.predictors -- a number of independent variables used to predict the response
        self.SVR -- a fitted support vector regression model
        self.tree -- a fitted ensemble tree model
        self.ridge -- a fitted Bayesian Ridge regression model
        """
        self.response = ""
        self.predictors = []
        self.setpoints = []
        self.SVR = None
        self.tree = None
        self.ridge = None

    def readCSV(self, data):
        """Parses a csv via pandas

        A csv is parsed and stored in the variable self.dataBox, self is
        returned to support method chaining.

        Keyword arguments:
        data -- the filename of a csv containing hourly output of an energy model
        """
        self.dataBox = pandas.read_csv(data, parse_dates=True)
        return self

    def addPredictor(self, predictor, isSetpoint = False):
        """Adds an independent variable to the list of predictors. If isSetpoint is set to true,
        add the predictor to the list of setpoints as well.

        Keyword arguments:
        predictor -- a string representing the name of a column in a corresponding csv file
        """
        self.predictors.append(predictor)
        if isSetpoint:
            self.setpoints.append(predictor)
        return self

    def setResponse(self, response):
        """Sets the response variable of the meta model

        Keyword arguments:
        response -- a string representing the name of a column in a corresponding csv file
        """
        self.response = response
        return self

    def fitSVR(self, cost, epsilon):
        """Initializes a support vector regression model

        Creates the SVR model that will be fitted to the provided data and returns self.
        Accepts two tuning parameters, cost and epsilon.

        Keyword arguments:
        cost -- tuning parameter (float)
        epsilon -- tuning parameter (float)
        """
        model = SVR(C=cost, epsilon = epsilon)
        self.SVR = model
        return self

    def bayesRidge(self):
        """Initializes a Bayesian Ridge regression model

        Creates the bayesRidge model that will be fitted to the provided data and returns self.
        """
        model = BayesianRidge()
        self.ridge = model
        return self

    def trees(self, treeDepth=4, numberOfTrees=100):
        """Initializes a boosted regression tree model

        Creates the Ada boosted regression tree model to be fitted to the provided data and returns self.
        Accepts parameters to indicate the depth of the tree (leaves) and the
        number of trees to incorporate into the ensemble.

        Keyword arguments:
        treeDepth -- indicates the max depth of fitted regression trees. Default = 4
        numberOfTrees -- boosting parameter indicating the number of trees to generate. Default = 100
        """
        rando = np.random.RandomState(1)
        boostedFit = AdaBoostRegressor(DecisionTreeRegressor(max_depth=treeDepth), n_estimators=numberOfTrees, random_state = rando)
        self.tree = boostedFit
        return self

    def getScores(self):
        """Fits the data to all initialized models and finds the cross validated score of each

        Requires the predictors and response variables to be set as well as a data set
        to be loaded and at least one model initialized. Creates the instance variable
        self.scores to which the cross validated score of each model is added for the sake of comparison.
        Returns self to facilitate method chaining.
        """
        X = self.dataBox[self.predictors]
        y = self.dataBox[self.response]
        self.scores = {}
        if (self.SVR is not None):
            self.scores['svr'] = cross_val_score(self.SVR, X, y).mean()
        if (self.tree is not None):
            self.scores['trees'] = cross_val_score(self.tree, X, y).mean()
        if (self.ridge is not None):
            self.scores['ridge'] = cross_val_score(self.ridge, X, y).mean()
        return self

    def fit(self, model):
        """
        Pass in one of the available learning models (SVR, ridge regression or boosted regression trees) to set as the fit for this object instance.
        The fitted model is set as self.fit and the cross validation score is printed. Return self to support method chaining.
        """
        X = self.dataBox[self.predictors]
        y = self.dataBox[self.response]
        self.model = model.fit(X, y)
        print('cross validation score: {0:.5f}'.format(cross_val_score(model, X, y).mean()))
        return self

    def predict(self, data):
        """
        Using the method with the best fit, we predict the behavior of the response
        variable(s) given a set of data containing weather predictions as well as
        a setpoint candidate vector

        Unlike most methods, does not return self, just a matrix of predicted values.
        """
        return self.model.predict(data)


    def persistMeta(self, fileName='meta.p'):
        """Simple pickle method, accepts a file name

        Keyword arguments:
        fileName -- a string for naming the pickle. Default = 'meta.p'
        """
        pickle.dump(self, open(fileName, 'wb'))

    def plotPredictions(self):
        """Generic plot routine
        """
        X = self.dataBox[self.predictors]
        y = self.dataBox[self.response]
        simTime = self.dataBox["Date/Time"]
        sim = self.dataBox.index.tolist()
        plt.plot(sim, y, c='b', label='E+')
        plt.hold('on')
        if (self.SVR is not None):
            svr = self.SVR.fit(X,y).predict(X)
            plt.plot(sim, svr, c='g', label='Meta-SVR')
        if (self.tree is not None):
            pass
        if (self.ridge is not None):
            pass
        plt.xlabel('Simulation Time')
        plt.ylabel(str(self.response))
        plt.legend()
        plt.show()
        return self
"""
ToDo:
- Create methods for performing SA with boosted trees
- Improve GCV scoring methods (make sure GCV is really being used...)
- Add features to optimize SVR fits (cost and epsilon)
- Add visualization features!
- Add features for additional data layers
- Add support for multiple kernals for SVR
"""
