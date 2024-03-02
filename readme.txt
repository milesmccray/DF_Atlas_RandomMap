Thanks for using the Atlas Randomizer. This was mostly a "for-fun" project to
allow easy-rating of maps on atlas. It's not perfect or really intended to
ACTUALLY be used. It gathers all visible atlas levels and assigns them a
difficulty based on the number of clears. Then based on your chosen criteria is
gives you a random map auto-launching dustforce / opening atlas.dustforce.com

It should work out-of the box, but if you ever need to redownload data make sure
to
    - Set "download_data" to "True" in the config.ini
    - Relaunch

    === OR ====

If you want to do a first-time setup,
    - Set the "first_time_setup" to "True" in the ini file and make sure to
      delete any user-related values in the ini file and the levels_data.json
      file.
    - Relaunch

If you have any questions contact on Discord @ mc_miles



=========INCASE config.ini GETS DELETED===========
[VALUES]
level_data = ./data/level_data.json
first_time_setup = true
download_data = false

[DATA]
download_date =
user_id =