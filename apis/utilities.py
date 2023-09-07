# import collections
# import pandas as pd
import traceback

def get_file_path(file_name):
    import os
    import sys
    dir_path = os.path.dirname(sys.argv[0])
    return os.path.join(dir_path, file_name)

def get_image_html(image_url:str, width='300px'):
    return '<img style="width:{width};" src="{url}" />'.format(width=width, url=image_url)

def get_link_html(url:str):
    return '<a href="{url}">{url}</a>'.format(url=url)

def get_error_message(e, url=None):
    errors = []
    if url:
        errors.append('This URL is invalid: ' + url)
    tokens = traceback.format_exc().split('\n')
    if len(tokens):
        errors.extend(tokens[0:3])
    return '\n'.join(errors)

def modify_system_path():
    import os, sys, inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir) 
