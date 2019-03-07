class TextParser(object):
    """
    A class containing methods used for parsing lists of data. Keeps the main
    script clean.
    """
    @staticmethod
    def kanji_deck_only_main_vocab_word(lst):
        """
        All of the text in each card of the Kanji deck is separated by
        '\x1f' characters. This method cleanly separates the unneeded
        information from those flashcards, returning only the first
        vocabulary word learned from the card and nothing else.
        """
        tmp = []
        for note_data in lst:
            tmp.append(note_data[0].split("\x1f")[4])
        return TextParser.__get_usable_vocab(tmp)

    @staticmethod
    def __get_usable_vocab(lst):
        """
        At this point, each piece of vocab in the list could contain
        multiple words separated by commas e.g. one, the thing, it etc.
        This function returns a list of vocab where only the first
        word is kept (since this is the important one for searching
        the sentence deck)
        """
        usable_vocab = []
        for v in lst:
            if ", " in v:
                v = v.split(", ")[0]
            if "<div>" in v:
                v = v[5:]
            usable_vocab.append(v)
        return usable_vocab