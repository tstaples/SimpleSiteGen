import json

FILETYPES = "filetypes"

class Config(object):
	def __init__(self, path):
		self._filetypes = []
		self.load(path)


	@property
	def filetypes(self):
	    return self._filetypes
	

	def load(self, path):
		try:
			jdata = json.load(open(path, 'r'))
		except Exception as e:
			raise Exception("Failed to read config file: " + str(e))

		if FILETYPES in jdata:
			self._filetypes = jdata[FILETYPES]
