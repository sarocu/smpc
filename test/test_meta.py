from meta import MetaModel
import pickle

def test_readCSV(data):
    model = MetaModel()
    model.readCSV(data)
    print(model.dataBox[:3])

def test_addPredictor():
    model = MetaModel()
    model.addPredictor("temperature")
    print(model.predictors)

def test_setResponse():
    model = MetaModel()
    model.setResponse("energy")
    print (model.response)

def test_fitSVR(data):
    model = MetaModel().readCSV(data)
    model.setResponse("Electricity:Facility [J](Hourly)")
    model.addPredictor("Environment:Site Outdoor Air Drybulb Temperature [C](Hourly)")
    model.addPredictor("Environment:Site Outdoor Air Humidity Ratio [kgWater/kgDryAir](Hourly)")

    model.fitSVR(cost=10, epsilon=0.2).getScores()
    print(model.scores)

def test_persist(data):
    model = MetaModel().readCSV(data)
    model.setResponse("Electricity:Facility [J](Hourly)")
    model.addPredictor("Environment:Site Outdoor Air Drybulb Temperature [C](Hourly)")
    model.addPredictor("Environment:Site Outdoor Air Humidity Ratio [kgWater/kgDryAir](Hourly)")

    model.fitSVR(cost=10, epsilon=0.2).getScores()

    model.persistMeta('testPickle.p')
    newModel = pickle.load(open('testPickle.p', 'rb'))
    print(newModel.scores)

def test_trees(data):
    model = MetaModel().readCSV(data)
    model.setResponse("Electricity:Facility [J](Hourly)")
    model.addPredictor("Environment:Site Outdoor Air Drybulb Temperature [C](Hourly)")
    model.addPredictor("Environment:Site Outdoor Air Humidity Ratio [kgWater/kgDryAir](Hourly)")

    model.trees(numberOfTrees=500).getScores()
    print(model.scores)

def test_ridge(data):
    model = MetaModel().readCSV(data)
    model.setResponse("Electricity:Facility [J](Hourly)")
    model.addPredictor("Environment:Site Outdoor Air Drybulb Temperature [C](Hourly)")
    model.addPredictor("Environment:Site Outdoor Air Humidity Ratio [kgWater/kgDryAir](Hourly)")

    model.bayesRidge().getScores()
    print(model.scores)

def test_all(data):
    model = MetaModel().readCSV(data)
    model.setResponse("Electricity:Facility [J](Hourly)")
    model.addPredictor("Environment:Site Outdoor Air Drybulb Temperature [C](Hourly)")
    model.addPredictor("Environment:Site Outdoor Air Humidity Ratio [kgWater/kgDryAir](Hourly)")
    model.addPredictor("BASEMENT:Zone Thermostat Heating Setpoint Temperature [C](Hourly)")
    model.addPredictor("CORE_MID:Zone Thermostat Heating Setpoint Temperature [C](Hourly)")
    model.addPredictor("CORE_TOP:Zone Thermostat Cooling Setpoint Temperature [C](Hourly)")

    model.bayesRidge().fitSVR(cost=10, epsilon=0.2).trees(numberOfTrees=300).getScores()
    print(model.scores)
    model.fit(model.SVR)
    model.persistMeta('../../data/demoMeta.p')

    #model.plotPredictions()

test_all("../../data/setpointsAndData.csv")
