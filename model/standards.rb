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
	def scaffold(prototype={:type=>'largeoffice', :vintage=>2017, :climatezone=>'5B'})
		@ashraeClimateZone = 'ASHRAE 169-2006-' + prototype[:climatezone]
		set_template(prototype[:vintage])
		@model.create_prototype_building(prototype[:type], @template, @ashraeClimateZone, @weatherfile)
	end

	# Set the template instance variable and collect the standard data for it
	def set_template(vintage=2017)
		standard = ''
	    if vintage < 1980
	      standard = 'DOE Ref Pre-1980'
	    elsif vintage >= 1980 and @vintage < 2004
	      standard = 'DOE Ref 1980-2004'
	    elsif vintage >= 2004 and @vintage < 2007
	      standard = '90.1-2004'
	    elsif vintage >= 2007 and @vintage < 2010
	      standard = '90.1-2007'
	    elsif vintage >= 2010 and @vintage < 2013
	      standard = '90.1-2010'
	    elsif vintage >= 2013
	      standard = '90.1-2013'
	    else
	      standard = 'none'
	    end

    	@template = standard
	end

	#
	def set_weather(weatherpath='./')
		@weatherfile = weatherpath
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
		return @model
	end


end