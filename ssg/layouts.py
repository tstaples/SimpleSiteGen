import utils

LAYOUTS = "layouts"

class Layouts(object):
	def __init__(self, path):
		self.layouts = dict()
		self.layouts_dir = path + LAYOUTS + "/"
		self.discover_layouts()


	def discover_layouts(self):
		for layout in utils.walk_folder(self.layouts_dir):
			self.layouts[layout] = ""


	def get_layout(self, name):
		layout = None
		if name in self.layouts:
			# Load the layout if it hasnt been yet
			if not self.layouts[name]:
				self.layouts[name] = utils.get_file_lines(self.layouts_dir + name)
			layout = self.layouts[name]
		return layout


	def layout_exists(self, name):
		return (name in self.layouts)


	def get_formatted_layout(self, layout_name, num_tabs):
		return Layouts.format_layout(self.get_layout(layout_name), num_tabs)


	@staticmethod
	def format_layout(layout_data, num_tabs):
		formatted_lines = []
		for line in layout_data:
			tabs = "".join("\t" for i in range(num_tabs))
			formatted_lines.append(tabs + line)
		# add a newline to the last line if there isn't one
		if not formatted_lines[-1].endswith("\n"):
			formatted_lines[-1] += "\n"
		return formatted_lines