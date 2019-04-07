from databasehelper import DatabaseHelper
from textparser import TextParser

def update_cards_to_study_in_database(learned_words):
    """
    First runs a query to get the sort field (id) of the sentences
    that you haven't learned. It then filters this down using the 
    previously obtained list of vocab that you HAVE learned, and
    returns a query that can be run to update all of the cards that
    you can now learn.
    """
    suspended = __get_unstudied_sentence_card_ids()
    doable_cards = __get_all_doable_sentence_card_vocabulary(learned_words)

    doable_ids = [c for c in doable_cards if c in suspended]

    if not doable_ids:
        print("There are no doable new cards to unsuspend. Have fun!")
        return
    else:
        id_lst = ", ".join(TextParser.all_elements_int_to_string(doable_ids))
        __update_database_unsuspend_doable_cards(id_lst)

def __update_database_unsuspend_doable_cards(final_id_lst):
    '''
    Gets all of the Sort ID's for the cards that contain
    only the vocabulary that you have learned. Then it 
    generates a query which will update all of the cards
    that you need to learn by un-suspending them and setting
    them to 'New'. The query is as follows:
    '''
    query = "update cards "
    query += "set queue = 0, type = 0 "
    query += "where nid in  "
    query += "( "
    query += "select id  "
    query += "from notes  "
    query += f"where sfld in ({final_id_lst}) "
    query += ") "
    query += "and did = 1547537208241"
    DatabaseHelper.execute(query)
    print(f"The following sentence cards were unsuspended:\n{final_id_lst}")

def __get_unstudied_sentence_card_ids():
    # Get the IDs of the sentence cards that I haven't yet studied (susp. cards)
    query = "select n.sfld "
    query += "from cards c "
    query += "join notes n on c.nid = n.id "
    # The below will restrict the selection of suspended cards to 'type = new'
    #query += "where c.type in 0 "
    #query += "and c.queue = -1 "
    query += "where c.queue = -1 "
    query += "and c.did = 1547537208241 "
    query += "order by n.sfld"
    return TextParser.for_each_trim_to_first(DatabaseHelper.execute(query))

def __get_all_doable_sentence_card_vocabulary(learned_words):
    # Get literally all of the card info in the sentences deck
    query = "select n.flds "
    query += "from cards c "
    query += "join notes n on c.nid = n.id "
    query += "where c.did = 1547537208241 "
    query += "order by n.sfld"
    query_results = DatabaseHelper.execute(query)
    return TextParser.for_each_get_doable_ids(query_results, learned_words)

def get_learned_rtk_kanji():
    '''
    This method will return all of the words that you have learned from the
    RTK kanji deck as a list, using the below query.
    '''
    query = "select n.flds "
    query += "from cards c "
    query += "join notes n on c.nid = n.id "
    query += "where c.type in (1,2) "
    query += "and c.did = 1554632049429"
    vocab = DatabaseHelper.execute(query)
    return TextParser.kanji_deck_only_main_vocab_word(vocab)

if __name__ == '__main__':
    learned_words = get_learned_rtk_kanji()
    update_cards_to_study_in_database(learned_words)