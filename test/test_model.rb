require_relative '../model/standards'
require_relative '../model/modelmanager'

model = StandardModel.new
model.set_weather('../data/USA_CO_Denver.Intl.AP.725650_TMY3.epw')
prototype = {
	:type=>'SmallHotel',
	:vintage=>2017,
	:climatezone=>'5B'
}
model.scaffold(prototype)

manager = ModelManager.new(model)
manager.create_workflow
manager.simulate