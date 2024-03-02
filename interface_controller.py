import json
import random
import urllib.error
import urllib.request
import shutil
import sys
from datetime import datetime
from config_manager import get_value, update_value
from level_data_downloader import download_user_data


def check_data_download():
	"""Checks if download_data is set to True in ini file."""
	download_data = get_value('VALUES', 'download_data')
	if download_data:
		# Download User Data
		download_user_data()

		# Sets INI File Variables
		update_value('VALUES', 'download_data', 'false')

		download_date = str(datetime.today().strftime('%F'))
		update_value('DATA', 'download_date', download_date)


def get_random_map(author, difficulty, ss):
	"""Gets a random ID from atlas_level_data.json."""

	level_list = []
	level_data_loc = get_value('VALUES', 'level_data')
	try:
		with open(level_data_loc, 'r') as f:
			level_set = json.load(f)
			for level in level_set:
				if level_set[level]['author'].lower() == author or author == '':
					if level_set[level]['level_dif'].lower() == difficulty or difficulty == 'all':
						if level_set[level]['user_ss'] != ss:  # Note: Inverse boolean
							level_list.append(level_set[level])
						else:
							continue
					else:
						continue
				else:
					continue

			random_map_data = random.choice(level_list)
			level_matches = len(level_list)

			# Downloads the level thumbnail and assigns it to ./data/current_level_thumbnail.png
			download_level_thumbnail(random_map_data)

		return random_map_data, level_matches
	except FileNotFoundError:
		print('level_data.json file is not found. Make sure "download_data" or "first_time_setup" '
			  'is set to True in config.ini or make sure level_data.json is located inside data '
			  'folder')
		sys.exit()


def get_random_map_all():
	"""Gets a random map from ALL random maps (only if "All Maps" is selected on GUI)."""

	level_list = []
	level_data_loc = get_value('VALUES', 'level_data')

	with open(level_data_loc, 'r') as f:
		level_set = json.load(f)
		for level in level_set:
			level_list.append(level_set[level])

	random_map_data = random.choice(level_list)
	level_matches = len(level_list)

	return random_map_data, level_matches


def download_level_thumbnail(random_map_data):
	"""Downloads the level thumbnail from atlas.dustforce.com ."""
	try:
		# Replaces any spaces in the level name with a "-"
		level_name = random_map_data["name"].replace(' ', '-')
		urllib.request.urlretrieve(f'http://atlas.dustforce.com/gi/maps/{level_name}-'
								   f'{random_map_data["atlas_id"]}.png',
								   './data/current_level_thumbnail.png')
	except urllib.error.HTTPError:
		try:
			# Replaces any spaces in the level name with a "%20" (This catches old maps)
			level_name = random_map_data["name"].replace(' ', '%20')
			urllib.request.urlretrieve(f'http://atlas.dustforce.com/gi/maps/{level_name}-'
									   f'{random_map_data["atlas_id"]}.png',
									   './data/current_level_thumbnail.png')
		except urllib.error.HTTPError:
			shutil.copy('./data/error_level_thumbnail.png', './data/current_level_thumbnail.png')
