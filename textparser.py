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
        tmp = [note_data[0].split("\x1f")[1] for note_data in lst]
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
        return [TextParser.__get_usable_vocab_trim(v) for v in lst]

    @staticmethod
    def __get_usable_vocab_trim(v):
        if ", " in v:
            return v.split(", ")[0]
        elif "<div>" in v:
            return v[5:]
        else:
            return v


    @staticmethod
    def for_each_trim_to_first(query_results):
        """
        The query which gets the sort field (IDs) (of all the sentence
        cards that you haven't learned) returns them in a strange format
        where every element in the results list is a tuple with one element.
        This gets the first element from each tuple and puts it in a list
        and returns that.
        """
        return [e[0] for e in query_results]

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
        learned_words_set = set(learned_words)
        query_results = TextParser.for_each_trim_to_first(query_results)
        for note in query_results:
            if note.split("\t")[0].split("\x1f")[4].split(", ") == ['']:
                continue
            current_vocabs = set(note.split("\t")[0].split("\x1f")[4].split(", "))
            if current_vocabs.issubset(learned_words_set):
                tmp.append(note.split("\t")[0].split("\x1f")[1])
        return TextParser.all_elements_string_to_int(tmp)

    @staticmethod
    def all_elements_string_to_int(lst):
        """
        Convert every element in a list into an integer from a string
        """
        return [int(e) for e in lst]

    @staticmethod
    def all_elements_int_to_string(lst):
        """
        Convert every element in a list into a string from an integer
        """
        return [str(e) for e in lst]
