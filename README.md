# CS-110-project-
Spotify recommendation app. The "music_finder.py" file has the main code for the app. 

The recommendation app has the following features:
- Allows the user to select one or more genres of music:
  - Present the user with a list of available genres using the spotify.get_genres_abridged() function
  - Ask the user to select one or more genres and store their genre selections in a list variable called “genres”
- Allows the user to select one or more artists:
  - Using the spotify.get_artists() function, provides a way for the user to search for and display artists 
  - Provides a way for the user to select the artists they’re interested in and store the corresponding artist objects in a list variable called “artists”
  - Allows the user to either clear out or append artists to their artists list
- Generate and email song recommendations:
  - Retrieves the recommended tracks using the spotify.get_similar_tracks() function
  - Prints the retrieved tracks to the screen in coherent format (using a pandas dataframe)
  - Asks the user if they want to email the tracks to someone, and if so, send an email of the list of track recommendations
  - Uses the spotify.get_formatted_tracklist_table_html() function to build a nice tracklist (see the video) that can be emailed
    
Libraries: pandas, spotify, twilio
