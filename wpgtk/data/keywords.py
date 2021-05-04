import configparser
from os import path

from .config import user_keywords, write_conf
from .files import get_keywords_path

KEY_LENGTH = 5
VAL_LENGTH = 2


def create_keywords_file(colorscheme):
    """creates a new keywords file and sets defaults if they exist"""
    parser = configparser.ConfigParser()
    parser.add_section('keywords')

    for k, v in dict(user_keywords):
        parser['keywords'][k] = v

    with open(get_keywords_path(colorscheme), "w") as keyword_file:
        parser.write(keyword_file)

    return get_keywords_path(colorscheme)


def get_keywords_section(colorscheme):
    """get keyword file configparser for current wallpaper
       or create one if it does not exist"""

    if colorscheme is None:
        return user_keywords

    parser = configparser.ConfigParser()

    if not path.isfile(get_keywords_path(colorscheme)):
        create_keywords_file(colorscheme)

    parser.read(get_keywords_path(colorscheme))
    return parser['keywords']


def update_key(old_keyword, new_keyword, colorscheme=None):
    """validates and updates a keyword for a wallpaper"""
    if not new_keyword:
        raise Exception('Keyword must be longer than 5 characters')

    keywords = get_keywords_section(colorscheme)
    keywords[new_keyword] = keywords[old_keyword]

    if (old_keyword != new_keyword):
        keywords.pop(old_keyword, None)

    write_keyword_file(keywords, colorscheme)


def update_value(keyword, value, colorscheme=None):
    """update the value to replace the user defined keyword with"""
    if not value:
        raise Exception('Value must exist')

    keywords = get_keywords_section(colorscheme)
    keywords[keyword] = value

    write_keyword_file(keywords, colorscheme)


def create_pair(keyword, value, colorscheme=None):
    """create a key value pair for a wallpaper"""
    if not value:
        raise Exception('There must be a value')

    if not keyword:
        raise Exception('There must be a keyword')

    keywords = get_keywords_section(colorscheme)
    keywords[keyword] = value

    write_keyword_file(keywords, colorscheme)


def remove_pair(keyword, colorscheme=None):
    """removes a pair of keyword value for a wallpaper"""

    keywords = get_keywords_section(colorscheme)
    keywords.pop(keyword, None)

    write_keyword_file(keywords, colorscheme)


def write_keyword_file(keywords, colorscheme=None):
    if colorscheme:
        keywords_path = get_keywords_path(colorscheme)
        parser = configparser.ConfigParser()
        parser['keywords'] = keywords

        with open(keywords_path, "w") as keyword_file:
            parser.write(keyword_file)
    else:
        write_conf()
