from .config import user_keywords, write_conf

KEY_LENGTH = 5
VAL_LENGTH = 2


def update_keyword(old_keyword, new_keyword, save=False):
    """validates and updates a keyword"""
    if not new_keyword:
        raise Exception('Keyword must be longer than 5 characters')

    user_keywords[new_keyword] = user_keywords[old_keyword]

    if(old_keyword != new_keyword):
        user_keywords.pop(old_keyword, None)

    if save:
        write_conf()


def update_value(keyword, value, save=False):
    if not value:
        raise Exception('Value must exist')

    user_keywords[keyword] = value

    if save:
        write_conf()


def create_pair(keyword, value, save=False):
    if not value:
        raise Exception('There must be a value')

    if not keyword:
        raise Exception('There must be a value')

    user_keywords[keyword] = value

    if save:
        write_conf()
