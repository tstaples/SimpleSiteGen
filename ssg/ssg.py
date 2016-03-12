import os
import inspect
import sys
import argparse

from config import Config
from layouts import Layouts
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


def build(params):
	force = params.force
	verbose = params.verbose
	target_directory = utils.normalize_path(params.target_directory)
	output_directory = utils.normalize_path(params.output_directory)
	config_directory = utils.normalize_path(params.config)
	config = Config(config_directory)
	layouts = Layouts(target_directory)


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

	print "root: " + root_path

	args.run(args)