import urllib.request
from urllib.request import urlopen
import json
try:
    import utilities
    utilities.modify_system_path()
except:
    pass

# Handles security:
def _get_token():
    url = 'https://www.apitutor.org/youtube/key' # authenticates to Spotify
    results = urlopen(url).read().decode('utf-8', 'ignore')
    return json.loads(results)['token']

def _simplify(data):
    try:
        data['items'][0]
    except Exception:
        return data

    simplified = []
    for item in data['items']:
        simplified.append({
            'videoId': item['id']['videoId'],
            'thumb_url': item['snippet']['thumbnails']['high']['url'],
            'title': item['snippet']['title'],
            'url': 'https://www.youtube.com/watch?v=' + item['id']['videoId'],
            'embed_url': 'https://www.youtube.com/embed/' + item['id']['videoId'],
            'share_url': 'https://www.youtube.com/' + item['id']['videoId']
        })
    return simplified


def get_videos(search_term, simplify=True):
    '''
    Retrieves a list of YouTube videos.
        * search_term (str): Required search term
        * simplify (bool):   Indicates whether you want to simplify the data that is returned.
    Returns a list of YouTube videos.
    '''
    search_term = urllib.parse.quote_plus(search_term)
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=' + search_term + '&type=video&key=' + _get_token()
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8', 'ignore'))
    if not simplify:
        return data
    return _simplify(data)

def get_video_player_html(embed_url, width=560, height=315):
    '''
    Returns an HTML IFrame (str). Requires an embed_url (string) argument.
    '''

    return '''
    <iframe width="{width}" height="{height}" src="{embed_url}" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
    '''.format(width=width, height=height, embed_url=embed_url)

def get_image_html(image_url:str):
    return '<img src="url" />'.format(url=image_url)