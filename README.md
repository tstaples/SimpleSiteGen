SimpleSiteGen
=============

SimpleSiteGen (ssg) is a very simple and basic static site generator.

Why create another static site generator when there are already so many out there?
Because I only needed something extremely basic and thought writing my own would be more fun than spending time browsing for one.

It's main (and only) purpose is 'include' templates in html files.

Yes this could be easily/quickly be done with sed and/or other existing tools but python is fun.


## Installation

TODO

## How it works

As the name implies it is very simple. 
You have your layouts which are typcially generic modules that appear in multiple places but remain mostly unchanged (ie. a nav bar).
You have your source (html) files where you use the ssg template syntax to refer to which layout you wish to include there.
Then you run the tool which evaulates and replaces the templates with the corresponding layouts and then exports everything to the target directory and bam, there's your site.

## Usage

SimpleSiteGen uses a very basic syntax for doing inclusions. It is just:

	{% include <layout name> %}

Where <layout name> is the name of a file in your project's 'layouts' directory (see Project Setup).

If you wish to comment out an ssg include then you can use the standard HTML comment syntax:
	
	<!-- {% include foo.html %} -->

## Project setup

Your project will need to include a few specific directories for ssg to be able to evaluate it. The project folder can contain whatever you want as long as it has the required dirs as well.

Here is an example of what the directory structure should look like:

	your_project_root/
		layouts/ 
			- layout templates that will be injected into your source files.
		public/
			- This is where the version of your site containing the ssg template syntax will be. Everything in here will be exported to the target dir and relevant files will also be parsed and evaluated.

## Commands

	ssg build [-f | -v] <target dir> <output dir>
		reads and evals the target dir and builds/exports to output dir.
		-f, --force: Overwrite the contents of the output directory if it exists.
		-v, --verbose: spits out more info about what's going on.
		target dir: location of the ssg compliant dir to eval.
		output dir: location of where to export the evaluated files.

	ssg init [-f | -v] <path>
		creates a skeleton directory structure for an ssg project.
		-f, --force: Overwrite the contents of the output directory if it exists.
		-v, --verbose: spits out more info about what's going on.
		path: where to create the skeleton directory.

## Future features

1. Basic state-based customization for layouts (ie. setting 'select' based on the page).

## Repo structure

	config/ - ignore file (doesn't need to be in target dir since only public is exported)
	ssg/ - main package source
	tests/ - unit tests