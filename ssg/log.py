level_none = 0
level_debug = 1
level_info = 2
level_warn = 3
level_error = 4

log_level_strings = ["Debug", "Info", "Warning", "Error"]

log_level = level_debug
log_file = "log" # default


def _log(level, msg):
	if level >= log_level:
		level_str = log_level_strings[level - 1]
		print("[" + level_str + "] " + msg)

def debug(msg):
	_log(level_debug, msg)

def info(msg):
	_log(level_info, msg)

def warn(msg):
	_log(level_warn, msg)

def error(msg):
	_log(level_error, msg)