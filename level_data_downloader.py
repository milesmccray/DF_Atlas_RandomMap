from bs4 import BeautifulSoup
import re
import requests
import json
from datetime import datetime
from config_manager import get_value, update_value


def download_user_data():
	"""Large download from dustkid.com that takes roughly 2 minutes to complete. Run sparingly."""

	print('Downloading User Data from dustkid.com... (This may take 1-2 minutes)')

	# Updates DATA Information in config ini
	update_value('VALUES', 'download_data', 'false')
	download_date = str(datetime.today().strftime('%F'))
	update_value('DATA', 'download_date', download_date)

	# Grabs Information from config ini
	user_id = get_value('DATA', 'user_id')
	level_data_loc = get_value('VALUES', 'level_data')

	# Grabs all visible levels from dustkid.com/levels.php and creates the base level_data.json
	grab_visible_levels()

	# Makes request to dustkid and grabs html
	request = requests.get(f'https://dustkid.com/profilecustom/{user_id}/')
	html = BeautifulSoup(request.content, 'html.parser')

	# Formats and combines user data with existing level_data.json
	level_list = format_user_data(html)
	level_data = level_difficulty(level_list)
	combine_data(level_data, level_data_loc)


def format_user_data(html):
	"""Formats the data to be inserted into level_data.json."""

	level_list = {}

	# Grabs the levels table (3rd <t> tag) from the html & just SS level data
	for levels in html.find_all('table')[2]:
		level = levels.find('td')
		flag = 0
		level_ss = {}

		# Checks for the junk lines at the start
		if level is not None and level != -1:
			url = level.find('a')
			scores = list(level.find_all('span', {'class': 'score scoreS'}))

			# Grabs level name-id by grabbing everything between / /
			pattern = r'level/(.*)/all'
			level_name_id = re.search(pattern, str(url)).group(1)

			# If level is not completed sets to false
			if not scores:
				level_ss['user_ss'] = False
				level_list[level_name_id] = level_ss

			# Checks for SS on every level and sets to True and creates the dictionary
			for score in scores:
				if '>S<' in str(score) and flag != 1:
					flag = 1
				if '>S<' in str(score) and flag == 1:
					level_ss['user_ss'] = True
					level_list[level_name_id] = level_ss
				else:
					level_ss['user_ss'] = False
					level_list[level_name_id] = level_ss

	return level_list


def level_difficulty(level_list):
	"""Assigns level difficulty based on number of clears according to dustkid.com/profilecustom
	as it is auto sorted by # of SS's. The weighting is just personal preference. The
	impossible_levels number is because there is roughly 1550 impossible levels. There are some
	levels that are not hidden on atlas despite being impossible, so this catches that"""

	num_levels = int((len(level_list)))
	easy_levels = round(num_levels * 0.45)  # 5629.05
	med_levels = round(num_levels * 0.30)  # 3752.7
	hard_levels = round(num_levels * .12)  # 1501.08
	impossible_levels = round(num_levels * .13)  # 1626.17
	i = 0
	flag = 0

	# Loops through each level and assigns it a difficulty based on its starting location in dict
	for level in level_list:
		# Easy Levels
		if i < easy_levels and flag == 0:
			i += 1
			level_list[level]['level_dif'] = 'easy'
			if i == easy_levels:
				i = 0
				flag = 1
				continue
		if i < med_levels and flag == 1:
			i += 1
			level_list[level]['level_dif'] = 'medium'
			if i == med_levels:
				i = 0
				flag = 2
				continue
		if i < hard_levels and flag == 2:
			i += 1
			level_list[level]['level_dif'] = 'hard'
			if i == hard_levels:
				i = 0
				flag = 3
				continue
		if i <= impossible_levels and flag == 3:
			i += 1
			level_list[level]['level_dif'] = 'impossible'
			continue

	return level_list


def combine_data(level_data, location):
	"""Combines the user_levels_ss with the existing visible levels pulled from dustkid."""

	try:
		level_data_copy = level_data.copy()
		# Deletes any levels in user_levels_ss that aren't visible
		with open(location, 'r') as file:
			atlas_level_data = json.load(file)
			for k in level_data_copy.keys():
				if k not in atlas_level_data.keys():
					del level_data[k]

		# Combines the two dictionaries based on the level Key
		for k, v in level_data.items():
			atlas_level_data[k].update(v)

		# Re-Writes the data into level_data.json
		with open(location, 'w') as f:
			json.dump(atlas_level_data, f, indent=3)
	except FileNotFoundError:
		print('location of level_data.json not found. check config.ini')


def grab_visible_levels():
	"""Grabs all visible levels from dustkid.com/levels.php by cycling through each page."""

	prev = False
	level_data_raw = {}

	while True:
		url = 'https://dustkid.com/levels.php?count=1024&prev='
		if prev:
			level_data_sec = requests.get(url + prev).json()
			prev = level_data_sec['next']
			level_data_raw.update(level_data_sec['levels'])
		elif prev is False:
			level_data_sec = requests.get(url).json()
			prev = level_data_sec['next']
			level_data_raw = level_data_sec['levels']
		elif prev is None:
			with open('data/level_data.json', 'w') as f:
				level_data = remove_false_levels(level_data_raw)
				json.dump(level_data, f, indent=3)
			break


def remove_false_levels(level_data_dirty):
	"""Removes all levels that are hidden (Only keeps VISIBLE ATLAS levels)."""

	level_data_clean = level_data_dirty.copy()
	for level in level_data_dirty:
		if level_data_dirty[level]['atlas_id'] == 0:
			del level_data_clean[level]
	return level_data_clean


if __name__ == '__main__':
	download_user_data()
