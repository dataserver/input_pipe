import unicodedata
import re


# normalizes a string into a caseless one
def normalize_caseless(text):
    if text is None:
        return "____none____"
    return unicodedata.normalize("NFKD", text.casefold())


# equal ignore case equivalent
def caseless_equal(left, right):
    return normalize_caseless(left) == normalize_caseless(right)


# a caseless re match
def re_match(my_str, r_exp):
    if r_exp is None:
        return False
    return re.search(r_exp, my_str, re.RegexFlag.IGNORECASE) is not None


def tree_fetch(first_order_func: callable, default=None):
    try:
        return first_order_func()
    except KeyError or IndexError:
        return default


DUMMY_DEFAULT = "__booga__"