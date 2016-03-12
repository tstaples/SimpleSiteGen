import utils

class Generator(object):
	def __init__(self, layouts):
		self.layouts = layouts


	def run(self, path):
		return self.parse_templates(path)


	def parse_templates(self, path):
		"""
		Looks for template syntax on each line and replaces it with the corresponding layout.
		"""
		new_lines = []
		lines = utils.get_file_lines(path)
		for line in lines:
			# check each line for the template syntax
			template, num_tabs = self.extract_template(line)
			if not template:
				new_lines.append(line)
				continue
			# concat the new lines added
			new_lines += self.eval_template(template, num_tabs)
		return new_lines


	def extract_template(self, line):
		"""
		Parses just the template syntax and number of indents from the line.
		"""
		template = (None, None)
		if len(line) == 0:
			return template
		# TODO: support closing brace on different line if needed
		beg = line.find("{% ")
		end = line.find(" %}")
		# check syntax is valid and not commented out
		if (beg > -1 and end > -1) and (end > beg) and not self.check_comments(line, beg, end):
			# keep track of how far it should be indented
			num_tabs = line[0:beg].count("\t")
			template = (line[beg + 3:end], num_tabs)
		return template


	def eval_template(self, template, num_tabs):
		"""
		Evaluates the contents of the template and executes the corresponding behaviour.
		"""
		lines = []
		parts = template.split(" ")
		# Specific to the one type for now since that's all there is.
		# TODO: handle template types generically if more are added
		if len(parts) < 2:
			log.error("Too few arguments in template: " + template)
			return lines

		# check the type
		template_type = parts[0]
		if template_type == "include":
			layout_name = parts[1]

			if not self.layouts.layout_exists(layout_name):
				log.error("no layout with name: " + layout_name)
			else:
				lines = self.layouts.get_formatted_layout(layout_name, num_tabs)
				if len(lines) == 0:
					log.error("no data for layout: " + layout_name)

		elif template_type == "Include":
			log.error("template type 'include' must be lower case.")
		else:
			log.error("unsupported template type: " + template_type)
		return lines


	def check_comments(self, line, beg, end):
		is_commented = False
		com_open_count = line.count("<!--")
		com_close_count = line.count("-->")
		prev_pos = 0
		for i in range(com_open_count):
			com_beg = line[prev_pos:].find("<!--")
			if com_beg < beg: # check if it starts before the template
				is_commented = True
				break
			prev_pos = com_beg

		if is_commented: # only check if we need to
			prev_pos = 0
			for i in range(com_close_count):
				com_end = line.find("-->")
				if com_end < beg: # if we find a closing one before the template assume it's not commented for now
					is_commented = False
				elif com_end > beg: # explicit check in case it's somehow -1
					is_commented = True
		return is_commented