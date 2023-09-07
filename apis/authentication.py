import requests
API_TUTOR_TOKEN ='API.fda8c628-f8f0-448d-aad8-42c2fcd067ec'


try:
    import utilities
    utilities.modify_system_path()
except:
    pass

def set_master_apitutor_token():
    '''Checks to make sure that you have included the API Tutor token in the my_token.py file.'''
    global API_TUTOR_TOKEN
    try:
        from apis import my_token
        API_TUTOR_TOKEN = my_token.API_TUTOR_TOKEN
    except:
        title = 'IMPORTANT: You Need an Access Token!'
        error_message = '\n\n\n' + '*' * len(title) + '\n' + \
            title + '\n' + '*' * len(title) + \
            '\nPlease download the the my_token.py file from Canvas and save it in your apis directory.\n\n'
        raise Exception(error_message)
set_master_apitutor_token()


def get_token(url):
    '''
    Retrieves the authentication token for the particular provider.

    * url (str): Required. The endpoint to the platform's token on API Tutor.  
    
    Returns the authentication token.
    '''
    response = requests.get(url + '?auth_manager_token=' + API_TUTOR_TOKEN)
    data = response.json()
    return data['token']
