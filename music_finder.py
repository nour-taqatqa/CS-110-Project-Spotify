from apis import spotify
from apis import twilio
import pandas

def print_menu():
    print('''
---------------------------------------------------------------------
Settings / Browse Options
---------------------------------------------------------------------
1 - Select your favorite genres  
2 - Select your favorite artists 
3 - Discover new music
4 - Quit
---------------------------------------------------------------------
    ''')

genres=[]  
counter=1

def handle_genre_selection():
    global counter
    print('\nHandle genre selection here...', '\n')
    genres_available=spotify.get_genres_abridged()
    for genre in genres_available:
        print(counter, '-',genre)
        counter+=1
    print('\nSelect one or more genres (type the number of the genre)')    
    
    user_genre_selection_01=int(input('\nFirst choice: '))
    genres.append(genres_available[user_genre_selection_01 - 1])

    while True:
        user_number_of_genres_to_choose=int(input('How many more genres would you like to choose ( 0, 1, or 2)? '))
        
        if  user_number_of_genres_to_choose ==1:
            user_genre_selection_02= int(input('Second choice: '))
            genres.append(genres_available[user_genre_selection_02 - 1])
            
        if user_number_of_genres_to_choose ==2:
            user_genre_selection_02= int(input('Second choice: '))
            user_genre_selection_03= int(input('Third choice: '))
            genres.append(genres_available[user_genre_selection_02 - 1])
            genres.append(genres_available[user_genre_selection_03 - 1])
            
        if user_number_of_genres_to_choose !=2 and user_number_of_genres_to_choose !=1 and user_number_of_genres_to_choose !=0:
            print('The number you entered is invalid, please enter either 0,1, or 2')
            continue
        print('Your genre choices are the following: ')
        for genre in genres:
            print(genre)
        decision_to_clear=input('Would you like to clear the list?(yes or no)')
        if decision_to_clear == 'yes':
            genres.clear()
            continue
        if decision_to_clear=='no':
            break

artists=[]
def handle_artist_selection():
    second_counter=0
    while True:
        choose_artist=input('Write down a name of an artist: ')

        spotify_artist_result=spotify.get_artists(choose_artist)
        print ('Here are the following artists that were found:','\n')
        for artist in spotify_artist_result:
            print(second_counter+1,'-',artist.get('name'))
            second_counter +=1
            
        what_artist_to_pick = input('\nFrom this list, type up to 3 artists you want to listen to (seperate names by a comma)')
        what_artist_to_pick_as_a_list= what_artist_to_pick.split(',')
        
        for choice in what_artist_to_pick_as_a_list:
            artists.append(choice)
        print ('Here are the artists you picked:')
        for element in artists:
            print( '---',element)
        
        decision_to_clear_or_add =input('\nWould you like to clear out the list or add more artists? (type "no", "clear out", or "add")')
        if decision_to_clear_or_add =='clear out':
            artists.clear()
            continue
        if decision_to_clear_or_add=="add":
            continue
        if decision_to_clear_or_add =="no":
            break

template = '''
    <html>
        <head><title>{name}</title></head>
        <body>
            <h1>{name}</h1>
            <p>Listen on <a href="{link}">Spotify</a></p>
            <img style="width: 400px;" src="{image}" />
        </body>
    </html>
'''
def get_recommendations():
    recommendations = spotify.get_similar_tracks(genres=genres)
    organized_table = pandas.DataFrame(recommendations)
    print (organized_table[['name','share_url']])


    email_or_not=input('Would you like to email this recommendation list? (yes or no)')
    if email_or_not == 'yes':
        organized_list_html =spotify.get_formatted_tracklist_table_html(recommendations)
        twilio.send_mail('nourtaqatqa2025@u.northwestern.edu',['nourtaqatqa2025@u.northwestern.edu','nour.s.taqatqa10@gmail.com'],
                         'Spotify recommendation list',organized_list_html)

# Begin Main Program Loop:
while True:
    print_menu()
    choice = input('What would you like to do? ')
    if choice == '1':
        handle_genre_selection()
    elif choice == '2':
        handle_artist_selection()
    elif choice == '3':
        get_recommendations() 
    elif choice == '4':
        print('Quitting...')
        break
    else:
        print(choice, 'is an invalid choice. Please try again.')
    print()
    input('Press enter to continue...')
