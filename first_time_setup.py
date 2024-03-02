import requests
from config_manager import update_value
from level_data_downloader import download_user_data


def first_time_setup():
	"""Sets initial values in config ini that are used in program and downloads user data."""

	user_id = check_user()
	update_value('VALUES', 'first_time_setup', 'false')
	update_value('DATA', 'user_id', user_id)
	download_user_data()


def check_user():
	"""Checks the given user if valid and returns json dictionary."""

	while True:
		URL = 'https://dustkid.com/profile/'
		user_id = input('What is your Dustkid ID: ')
		if user_id.isnumeric():
			try:
				page = requests.get(f'{URL}{user_id}/')
				if 'Profile - Cannot find user' in page.text:
					print(f'{user_id} is not a valid ID. Try again...\n')
					continue
				else:
					break
			except requests.exceptions.ConnectionError:
				print(f'No connection can be made to dustkid.com...\n')
				continue
		else:
			print(f'{user_id} is not a valid ID. Try again...\n')

	return user_id
