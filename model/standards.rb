require 'openstudio'
require 'openstudio-standards'

class StandardModel
	def initialize
		@model = OpenStudio::Model::Model.new
	end

	# Quickly create an openstudio model based on openstudio-standards
	#
	# inputs:
	# - building type [{:type=>buildingtype (string), :conditionedarea=>double (0..100.0)}, ...]
	# - vintage
	# - HVAC system type
	# - conditioned floor area
	def scaffold(buildingtypes=[{:type=>'largeoffice', :conditionedarea=>100.0}])

	end

	# Scale the standard geometry for the model to match the floor area given
	#
	# inputs:
	# - area (m^2)
	def scale_geometry(area)

	end

	# Create a baseline vav system and apply it to the model
	def make_vav_system

	end

	#
	def make_packaged_single_zone

	end

	#
	def make_packaged_heat_pump

	end

	#
	def make_split_system

	end

	# Return the associated model
	def get
		#
	end


end