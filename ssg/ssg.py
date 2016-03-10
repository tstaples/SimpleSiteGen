import os
import sys
import argparse
#import utils
#import log

def build(params):
	print params

def init(params):
	print params

parser = argparse.ArgumentParser(description="A very basic static site generator.")
parser.add_argument("-v", "--verbose", action="store_true", help="Output extra information.")
sub_commands = parser.add_subparsers(title="SimpleSiteGen commands", description="Entry points for ssg.")

build_command = sub_commands.add_parser("build", help="Evaluates the templates and exports the full site.")
build_command.add_argument("target_directory", nargs=1, help="Path to the ssg compliant directory to evaluate.")
build_command.add_argument("output_directory", nargs=1, help="Path to export the evaluated files to.")
build_command.add_argument("-f", "--force", action="store_true", help="Overwrite the contents of the output directory if it exists.")
build_command.set_defaults(run=build)

init_command = sub_commands.add_parser("init", help="Creates a skeleton directory structure for an ssg project.")
init_command.add_argument("target_directory", nargs=1, help="Path to where to initialize an ssg skeleton directory.")
init_command.set_defaults(run=init)


if  __name__ == "__main__":
	args = parser.parse_args()
	args.run(args)