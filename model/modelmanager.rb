require 'openstudio'
require 'openstudio-standards'
require 'sqlite3'
require 'json'
require 'fileutils'
require 'distribution'

# Model class provides a suite of helper functions for running simulations and creating a data set for fitting meta-models
class ModelManager
	# Load up an OSM file that we want to create a meta model from
	def initialize(model, seed=101)
		@model = model.get
		@pdfs = Hash.new
		@uncertain = Hash.new # for storing a reference between a variable to be perturbed and its pdf
		@seed = seed
	end

	# Create unique identifiers
	def make_random_id
		o = [('a'..'z'), ('A'..'Z')].map(&:to_a).flatten
    	return (0...50).map { o[rand(o.length)] }.join
	end

	# Add a given parameter to the E+ output
	def add_reporting_variables(param)

	end

	# Based on a series of run results, pick out variables to calibrate by
	def sensitivity_study
		# boosted regression trees...
	end

	# Create a OSW file for managing the simulation workflow, save to a file.
	def create_workflow(workflowpath='./')

	end

	# Randomly perturb variables and run a simulation, caching the results
	def peturb_and_run
		# do some stuff
		simulate
	end

	# Kick off a simulation
	def simulate
  		cli_path = OpenStudio.getOpenStudioCLI
    	cmd = "\"#{cli_path}\" run -w \"#{@osw_path}\""
    	puts cmd
    	system(cmd)
	end

	# Cache simulation results
	def collect_results
		# wraps a bunch of other methods that extract specific time series results
		# sync to either a DB or a big JSON file
	end

	# Return a probability density function for perturbing variables. Returns the key from the instance variable @pdfs
	def normal_pdf(mean=0, stdev=1)
		pdf = Distribution::Normal.rng(mean, stdev, @seed)
		key = make_random_id
		@pdfs[key] = pdf 
		return key
	end

	# Return a random number according to the referenced pdf
	def sample(key)
		pdf = @pdfs[key]
		return pdf.call
	end

	# Store simulation results for multiple runs in a standard format
	def persist(filename)

	end
end