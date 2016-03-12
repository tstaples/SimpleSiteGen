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
