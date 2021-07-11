import configparser
from os import path

from .config import user_keywords, write_keywords

KEY_LENGTH = 5
VAL_LENGTH = 2


def get_keywords_section(theme = None):
    """get keyword file configparser for current wallpaper
       or create one if it does not exist"""
    if theme is None:
        return user_keywords['default']

    if not user_keywords.has_section(theme):
        user_keywords.add_section(theme)
        user_keywords[theme] = user_keywords['default']

    return user_keywords[theme]

def reset_keywords_section(theme):
    """set the theme's keyword to the default key value pairs"""

    if user_keywords.has_section(theme):
        user_keywords[theme] = user_keywords['default']
        write_keywords()

def update_key(old_keyword, new_keyword, theme=None):
    """validates and updates a keyword for a wallpaper"""
    if not new_keyword:
        raise Exception('Keyword must be longer than 5 characters')

    keywords = get_keywords_section(theme)
    keywords[new_keyword] = keywords[old_keyword]

    if (old_keyword != new_keyword):
        keywords.pop(old_keyword, None)

    write_keywords()


def update_value(keyword, value, theme=None):
    """update the value to replace the user defined keyword with"""
    if not value:
        raise Exception('Value must exist')

    keywords = get_keywords_section(theme)
    keywords[keyword] = value

    write_keywords()


def create_pair(keyword, value, theme=None):
    """create a key value pair for a wallpaper"""
    if not value:
        raise Exception('There must be a value')

    if not keyword:
        raise Exception('There must be a keyword')

    keywords = get_keywords_section(theme)
    keywords[keyword] = value

    write_keywords()


def remove_pair(keyword, theme=None):
    """removes a pair of keyword value for a wallpaper"""

    keywords = get_keywords_section(theme)
    keywords.pop(keyword, None)

    write_keywords()
