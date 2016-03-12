import os
import inspect
import sys
import argparse

from config import Config
from layouts import Layouts
from generator import Generator
import utils
import log

''' 
	1. load config and read types into list if custom config file was not specified, else load theirs.
	2. check if target dir exists: if no throw exception
	3. look for layouts dir: can't find = error
		a. read in all the layout names (contents will be fetched on demand) and store in map (name, contents)
	4. look for public dir: can't find = error
	5. walk public and match files against types in list
	6. parse matched:
		a. check for include syntax
		b. if the layout wasn't loaded load it now and insert.
	7. output to output

'''


def create_output_directory(path, force):
	"""
	handles removal/creation of output directory.
	"""
	if utils.path_exists(path):
		# We'll assume that if it's empty we can write into it
		if utils.directory_empty(path):
			return True

		if not force:
			return False
		else:
			log.info("Removing previous contents of output directory...")
			utils.remove_directory(path)

	log.info("Creating output directory...")
	utils.create_directory(path)
	return True


def build(params):
	"""
	Main entry point for the build command.
	"""
	verbose = params.verbose
	target_directory = utils.normalize_directory(params.target_directory)
	output_directory = utils.normalize_directory(params.output_directory)
	config_directory = utils.normalize_path(params.config)
	config = Config(config_directory)
	layouts = Layouts(target_directory)
	generator = Generator(layouts)

	if not create_output_directory(output_directory, params.force):
		print "Output directory already exists. If you wish to overwrite it use -f."
		return False

	public_directory = utils.normalize_directory(target_directory + "public")
	for path in utils.walk_folder(public_directory):
		full_path = utils.normalize_path(public_directory + path)

		# check if we should parse this file or just copy it
		extension = utils.get_extension(full_path)
		if extension and extension in config.filetypes:
			data = generator.run(full_path)
			utils.write_list_to_file(output_directory + path, data)
			continue

		try:
			log.info("copying: " + full_path + " to " + output_directory + path)
			utils.copy_file(full_path, output_directory + path)
		except Exception as e:
			log.error("Error copying file")
			continue
	return True




def init(params):
	print params


root_path = utils.normalize_path(utils.get_current_dir() + "/")

parser = argparse.ArgumentParser(description="A very basic static site generator.")
parser.add_argument("-v", "--verbose", action="store_true", help="Output extra information.")
sub_commands = parser.add_subparsers(title="SimpleSiteGen commands", description="Entry points for ssg.")

build_command = sub_commands.add_parser("build", help="Evaluates the templates and exports the full site.")
build_command.add_argument("target_directory", help="Path to the ssg compliant directory to evaluate.")
build_command.add_argument("output_directory", help="Path to export the evaluated files to.")
build_command.add_argument("-f", "--force", action="store_true", help="Overwrite the contents of the output directory if it exists.")
build_command.add_argument("-cf", "--config", nargs=1, default=root_path + "../config/ssg_config.json", help="Path to custom ssg config file.")
#build_command.add_argument("-t", "--file-types", nargs="?", help="File types to parse explicitly.")
build_command.set_defaults(run=build)

init_command = sub_commands.add_parser("init", help="Creates a skeleton directory structure for an ssg project.")
init_command.add_argument("target_directory", nargs=1, help="Path to where to initialize an ssg skeleton directory.")
init_command.set_defaults(run=init)


if  __name__ == "__main__":
	args = parser.parse_args()

	# set log level based on verbose flag
	log.log_level = log.level_info if args.verbose else log.level_error

	if args.run(args):
		print "Operation completed successfully."
	else:
		print "Operation finished with errors."