from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""
    lines_a = set(a.splitlines())
    lines_b = set(b.splitlines())
    same_lines = set(lines_a.intersection(lines_b))
    return same_lines


def sentences(a, b):
    """Return sentences in both a and b"""
    sentences_a = set(sent_tokenize(a))
    sentences_b = set(sent_tokenize(b))
    same_sentences = set(sentences_a.intersection(sentences_b))
    return same_sentences


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    substrings_a = set(split_string(a, n))
    substrings_b = set(split_string(b, n))
    same_substrings = set(substrings_a.intersection(substrings_b))
    return same_substrings

def split_string(a, n):
    split_string = []
    for i in range(len(a) + 1 - n):
        split_string.append(a[i:i+n])
    return split_string
