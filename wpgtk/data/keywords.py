import configparser
from os import path

from .config import user_keywords
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

    return parser


def get_keywords_parser(colorscheme):
    """get keyword file configparser for current wallpaper
       or create one if it does not exist"""

    if colorscheme == None:
        parser = user_keywords
        return parser

    if path.isfile(get_keywords_path(colorscheme)):
        parser = configparser.ConfigParser()
        parser.read(get_keywords_path(colorscheme))

        return parser

    else:
        return create_keywords_file(colorscheme)


def update_key(colorscheme, old_keyword, new_keyword):
    """validates and updates a keyword for a wallpaper"""
    if not new_keyword:
        raise Exception('Keyword must be longer than 5 characters')

    parser = get_keywords_parser(colorscheme) if colorscheme else user_keywords
    keywords = parser['keywords']
    keywords[new_keyword] = keywords[old_keyword]

    if (old_keyword != new_keyword):
        keywords.pop(old_keyword, None)

    with open(get_keywords_path(colorscheme), "w") as keyword_file:
        parser.write(keyword_file)


def update_value(colorscheme, keyword, value):
    """update the value to replace the user defined keyword with"""
    if not value:
        raise Exception('Value must exist')

    parser = get_keywords_parser(colorscheme) if colorscheme else user_keywords
    keywords = parser['keywords']
    keywords[keyword] = value

    with open(get_keywords_path(colorscheme), "w") as keyword_file:
        parser.write(keyword_file)


def create_pair(colorscheme, keyword, value):
    """create a key value pair for a wallpaper"""
    if not value:
        raise Exception('There must be a value')

    if not keyword:
        raise Exception('There must be a keyword')

    parser = get_keywords_parser(colorscheme) if colorscheme else user_keywords
    parser['keywords'][keyword] = value

    with open(get_keywords_path(colorscheme), "w") as keyword_file:
        parser.write(keyword_file)


def remove_pair(colorscheme, keyword):
    """removes a pair of keyword value for a wallpaper"""

    parser = get_keywords_parser(colorscheme) if colorscheme else user_keywords
    parser['keywords'].pop(keyword, None)

    with open(get_keywords_path(colorscheme), "w") as keyword_file:
        parser.write(keyword_file)
