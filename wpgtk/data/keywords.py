from .config import keywords, write_conf

KEY_LENGTH = 5
VAL_LENGTH = 2


def update_keyword(old_keyword, new_keyword, save=False):
    """validates and updates a keyword"""
    if(len(new_keyword) < KEY_LENGTH):
        raise Exception('Keyword must be longer than 5 characters')

    keywords[new_keyword] = keywords[old_keyword]

    if(old_keyword != new_keyword):
        keywords.pop(old_keyword, None)

    if save:
        write_conf()


def update_value(keyword, value, save=False):
    if(len(value) < 2):
        raise Exception('Value must be longer than 3 characters')

    keywords[keyword] = value

    if save:
        write_conf()


def create_pair(keyword, value, save=False):
    if(len(value) < VAL_LENGTH):
        raise Exception('Value must be longer than 3 characters')

    if(len(keyword) < KEY_LENGTH):
        raise Exception('Value must be longer than 3 characters')

    keywords[keyword] = value

    if save:
        write_conf()
