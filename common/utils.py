import unicodedata


def normalize(txt):
    return strip_accents(txt).lower()


def strip_accents(txt):
    """
        odstraní diakritiku
    """
    def basechar(char):
        """
        odstraní diakritiku pro 1 znak
        """
        desc = unicodedata.name(char)
        cutoff = desc.find(' WITH ')
        if cutoff != -1:
            desc = desc[:cutoff]
        try:
            return unicodedata.lookup(desc)
        except KeyError:
            return char

    return ''.join(basechar(char) for char in txt)

    # toto je asi rychlejší+jednodušší, ale nefunguje pro strike písmena
    # return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
