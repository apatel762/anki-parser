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

    @staticmethod
    def for_each_trim_to_first(query_results):
        """
        The query which gets the sort field (IDs) (of all the sentence
        cards that you haven't learned) returns them in a strange format
        where every element in the results list is a tuple with one element.
        This gets the first element from each tuple and puts it in a list
        and returns that.
        """
        tmp = []
        for e in query_results:
            tmp.append(e[0])
        return tmp

    @staticmethod
    def for_each_get_doable_ids(query_results, learned_words):
        """
        The query which gets all of the sentence card vocabulary literally
        just returns all of the content on the card. This function will parse
        that raw data and get all of the card IDs that correspond to the
        card IDs that haven't been studied, but are doable given my current
        knowledge.
        It then returns a list of ids that can have their respective cards
        updated to match this.
        """
        tmp = []
        query_results = TextParser.for_each_trim_to_first(query_results)
        for note in query_results:
            if note.split("\t")[0].split("\x1f")[4].split(", ") == ['']:
                continue
            if set(note.split("\t")[0].split("\x1f")[4].split(", ")).issubset(learned_words):
                tmp.append(note.split("\t")[0].split("\x1f")[1])
        return tmp