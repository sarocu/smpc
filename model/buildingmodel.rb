require_relative './standards'

class BuildingModel < standards
	# Initialize the BuildingModel
	#
	# Optionally specify an existing openstudio model
	def initialize(model=nil)
		if model
			@model = model.get
		else
			super
		end
	end
end