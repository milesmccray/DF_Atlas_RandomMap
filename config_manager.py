from configparser import ConfigParser


def get_value(section, name):
	"""Returns the associated value in the config INI file."""
	config = ConfigParser()
	config.read('./data/config.ini')
	try:
		value = config.getboolean(section, name)
		return value
	except ValueError:
		value = config.get(section, name)
		return value


def update_value(section, name, new_value):
	"""Updates the associated value in the config INI file."""
	config = ConfigParser()
	config.read('./data/config.ini')
	cfgfile = open('./data/config.ini', 'w')
	config.set(section, name, new_value)
	config.write(cfgfile)
	cfgfile.close()
