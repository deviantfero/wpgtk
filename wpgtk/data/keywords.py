import configparser
from os import path

from .config import user_keywords, write_conf
from .files import get_keywords_path

KEY_LENGTH = 5
VAL_LENGTH = 2


def create_keywords_file(filename):
    """creates a new keywords file and sets defaults if they exist"""
    parser = configparser.ConfigParser()
    parser.add_section('keywords')

    for k, v in dict(user_keywords):
        parser['keywords'][k] = v

    with open(get_keywords_path(filename), "w") as keyword_file:
        parser.write(keyword_file)

    return get_keywords_path(filename)


def get_keywords_section(filename = None):
    """get keyword file configparser for current wallpaper
       or create one if it does not exist"""
    if filename is None:
        return user_keywords

    parser = configparser.ConfigParser()

    if not path.isfile(get_keywords_path(filename)):
        create_keywords_file(filename)

    parser.read(get_keywords_path(filename))

    return parser['keywords']


def update_key(old_keyword, new_keyword, filename=None):
    """validates and updates a keyword for a wallpaper"""
    if not new_keyword:
        raise Exception('Keyword must be longer than 5 characters')

    keywords = get_keywords_section(filename)
    keywords[new_keyword] = keywords[old_keyword]

    if (old_keyword != new_keyword):
        keywords.pop(old_keyword, None)

    write_keyword_file(keywords, filename)


def update_value(keyword, value, filename=None):
    """update the value to replace the user defined keyword with"""
    if not value:
        raise Exception('Value must exist')

    keywords = get_keywords_section(filename)
    keywords[keyword] = value

    write_keyword_file(keywords, filename)


def create_pair(keyword, value, filename=None):
    """create a key value pair for a wallpaper"""
    if not value:
        raise Exception('There must be a value')

    if not keyword:
        raise Exception('There must be a keyword')

    keywords = get_keywords_section(filename)
    keywords[keyword] = value

    write_keyword_file(keywords, filename)


def remove_pair(keyword, filename=None):
    """removes a pair of keyword value for a wallpaper"""

    keywords = get_keywords_section(filename)
    keywords.pop(keyword, None)

    write_keyword_file(keywords, filename)


def write_keyword_file(keywords, filename=None):
    if filename:
        keywords_path = get_keywords_path(filename)
        parser = configparser.ConfigParser()
        parser['keywords'] = keywords

        with open(keywords_path, "w") as keyword_file:
            parser.write(keyword_file)
    else:
        write_conf()
