import PySimpleGUI as sg
import webbrowser
import os
from interface_controller import get_random_map, get_random_map_all, check_data_download
from config_manager import get_value


def gui():
	"""Creates Main GUI."""

	# Checks if data needs downloaded before running GUI
	check_data_download()

	# Sets Defaults
	author = ''
	difficulty = 'All'
	ss = True
	random_map_data_startup, level_matches_startup = get_random_map(author, difficulty.lower(), ss)
	level_name = random_map_data_startup['name']
	author_name = random_map_data_startup['author']
	user_id = get_value('DATA', 'user_id')
	download_date = get_value('DATA', 'download_date')
	sg.theme('Black')

	# GUI "Layouts"
	level_image = [
		sg.Image('./data/current_level_thumbnail.png', enable_events=True, key='IMAGE')
	]
	user_information = [
		sg.Push(),
		sg.Text(f'User ID: {user_id}', font=('Arial Bold', 10)),
		sg.Text(f'Last Updated: {download_date}')
	]
	current_level_data = [
		sg.Text(f'{level_name}', font=('Arial Bold', 13),
				enable_events=True, key='CURRENT_LEVEL', text_color='plum1'),
		sg.Text(f'By: {author_name}', font=('Arial Bold', 13),
				enable_events=True, key='CURRENT_AUTHOR', text_color='orange1'),
		sg.Push(),
		sg.VerticalSeparator(),
		sg.Checkbox('Open Atlas', font=('Arial Bold', 12), default=True, enable_events=True,
					key='OPEN_ATLAS')
	]

	num_matches = [
		sg.Text(' Visible Level Matches:', font=('Arial Bold', 12), pad=(0, 0)),
		sg.Text(f'{level_matches_startup} levels', font=('Arial Bold', 14), pad=(0, 0),
				enable_events=True,
				key='NUM_LEVELS'),
		sg.Push(),
		sg.VerticalSeparator(),
		sg.Button('Play', font=('Arial Bold', 15), button_color=('White', 'DodgerBlue4'),
				  enable_events=True),
		sg.Button('Random', font=('Arial Bold', 15), button_color=('White', 'DodgerBlue4'))
	]

	h_seperator = [
		sg.HorizontalSeparator()
	]

	settings_1 = [
		sg.Checkbox("I haven't SS'ed", font=('Arial Bold', 12), default=ss, enable_events=True,
					key='SS'),
		sg.Text('Level Difficulty:', font=('Arial Bold', 12)),
		sg.Spin(['Hard', 'Medium', 'Easy', 'All'], font=('Arial Bold', 12), text_color='white',
				readonly=True, initial_value=difficulty, size=7, enable_events=True,
				key='DIFFICULTY'),
		sg.Push(),
		sg.Checkbox('All Maps', font=('Arial Bold', 12), enable_events=True, key='ALL'),

	]
	settings_2 = [
		sg.Text('Author:', font=('Arial Bold', 12), pad=(0, 0)),
		sg.InputText(size=15, enable_events=True, default_text=author, key='AUTHOR', pad=(0, 0)),
		sg.Button('Update', font=('Arial Bold', 10),
				  button_color=('White', 'DarkGreen'), enable_events=True, key='UPDATE_AUTHOR'),
		sg.Push(),
		sg.Button('Settings', font=('Arial Bold', 15), button_color=('White',
																				 'DarkGreen')),
		sg.Button('Quit', font=('Arial Bold', 15), button_color=('White', 'Brown2'))
	]
	layout = [
		level_image,
		user_information,
		current_level_data,
		num_matches,
		h_seperator,
		settings_1,
		settings_2
	]

	run_gui(layout, random_map_data_startup)


def run_gui(layout, random_map_data_startup):
	"""Runs the GUI by constantly checking for any events."""

	# Create the window
	window = sg.Window('Atlas Randomizer', layout)
	random_map_data = random_map_data_startup

	# Display and interact with the Window using an Event Loop
	while True:
		event, values = window.read()
		# Random Map Button
		if event == 'Random':
			try:
				# Re-Grabs all Values
				author = values['AUTHOR']
				difficulty = values['DIFFICULTY']
				ss = values['SS']

				# Gets random map ID & level matches
				random_map_data, level_matches = (
					get_random_map(author.lower(), difficulty.lower(), ss))

				# Updates Current Level & Author & Image
				window['CURRENT_LEVEL'].update(f'{random_map_data["name"]}')
				window['CURRENT_AUTHOR'].update(f'By: {random_map_data["author"]}')
				window['IMAGE'].update('./data/current_level_thumbnail.png')
			except IndexError:
				continue

		if event == 'Play':
			try:
				# Opens Atlas Link & Install and Play
				if values['OPEN_ATLAS']:
					webbrowser.open(f'http://atlas.dustforce.com/{random_map_data["atlas_id"]}/')
				webbrowser.open(f'dustforce://installPlay/{random_map_data["atlas_id"]}/')
			except:
				pass

		# All Button
		if event == 'ALL':
			all_value = values['ALL']
			try:
				if all_value is True:
					# Gets random map ID & level matches of ALL levels
					random_map_data, level_matches = get_random_map_all()

					# Updates NUM_LEVELS event
					window['NUM_LEVELS'].update(f'{level_matches} levels')

				else:
					# Re-Grabs all Values
					author = values['AUTHOR']
					difficulty = values['DIFFICULTY']
					ss = values['SS']

					# Gets random map ID & level matches
					random_map_data, level_matches = (
						get_random_map(author.lower(), difficulty.lower(), ss))

					# Updates NUM_LEVELS event
					window['NUM_LEVELS'].update(f'{level_matches} levels')

			except IndexError:
				# Updates NUM_LEVELS event with error text
				window['NUM_LEVELS'].update(f'0 levels')

		# Author
		if event == 'UPDATE_AUTHOR':
			all_value = values['ALL']
			if all_value is False:
				try:
					# Re-Grabs all Values
					author = values['AUTHOR']
					difficulty = values['DIFFICULTY']
					ss = values['SS']

					# Gets random map ID & level matches
					random_map_data, level_matches = (
						get_random_map(author.lower(), difficulty.lower(), ss))

					# Updates NUM_LEVELS event
					window['NUM_LEVELS'].update(f'{level_matches} levels')

				except IndexError:
					# Updates NUM_LEVELS event with error text
					window['NUM_LEVELS'].update(f'0 levels')
			else:
				# Do nothing because all_value is True
				continue

		# Difficulty
		if event == 'DIFFICULTY':
			all_value = values['ALL']
			if all_value is False:
				try:
					# Re-grabs all the values
					author = values['AUTHOR']
					difficulty = values['DIFFICULTY']
					ss = values['SS']

					# Gets random map ID & level matches
					random_map_data, level_matches = (
						get_random_map(author.lower(), difficulty.lower(), ss))

					# Updates NUM_LEVELS event
					window['NUM_LEVELS'].update(f'{level_matches} levels')

				except IndexError:
					# Updates NUM_LEVELS event with error text
					window['NUM_LEVELS'].update(f'0 levels')
			else:
				# Do nothing because all_value is True
				continue

		# Haven't SS'ed
		if event == 'SS':
			all_value = values['ALL']
			if all_value is False:
				try:
					# Re-grabs all the values
					author = values['AUTHOR']
					difficulty = values['DIFFICULTY']
					ss = values['SS']

					# Gets random map ID & level matches
					random_map_data, level_matches = (
						get_random_map(author.lower(), difficulty.lower(), ss))

					# Updates NUM_LEVELS event
					window['NUM_LEVELS'].update(f'{level_matches} levels')

				except IndexError:
					# Updates NUM_LEVELS event with error text
					window['NUM_LEVELS'].update(f'0 levels')
			else:
				# Do nothing because all_value is True
				continue

		# Settings Button
		if event == 'Settings':
			try:
				os.system('open ./data/config.ini')
			except:
				pass

		if event == sg.WINDOW_CLOSED or event == 'Quit':
			break

	window.close()


if __name__ == '__main__':
	check_data_download()
	gui()
