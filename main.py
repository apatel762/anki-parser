'''
Get all of the sort fields (IDs) of the vocab from the Japanese deck which 
are inside of new cards and put it into 'unlearned_vocab.txt':

select n.sfld
from cards c 
join notes n on c.nid = n.id
where c.type = 0
and c.queue = -1
and c.did = 1547537208241
order by n.sfld

Make sure to do both of the above steps before running the code in 
this file!
'''
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
    card_ids = __get_unstudied_sentence_card_ids()
    doable_sntnce_ids = __get_all_doable_sentence_card_vocabulary(learned_words)

    doable_new_cards_ids = []
    for c_id in doable_sntnce_ids:
        if c_id in card_ids:
            doable_new_cards_ids.append(c_id)

    if not doable_new_cards_ids:
        print("There are no doable new cards to unsuspend. Have fun!")
        return
    else:
        __update_database_unsuspend_doable_cards(doable_new_cards_ids)

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
    query += "where sfld in (" + ", ".join(final_id_lst) + ") "
    query += ") "
    query += "and did = 1547537208241"
    DatabaseHelper.execute(query)
    print(f"Database unsuspended {len(final_id_lst)} new cards")

def __get_unstudied_sentence_card_ids():
    query = "select n.sfld "
    query += "from cards c "
    query += "join notes n on c.nid = n.id "
    query += "where c.type = 0 "
    query += "and c.queue = -1 "
    query += "and c.did = 1547537208241 "
    query += "order by n.sfld"
    return TextParser.for_each_trim_to_first(DatabaseHelper.execute(query))

def __get_all_doable_sentence_card_vocabulary(learned_words):
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
    query += "where c.type = 2 "
    query += "and c.did = 1543218842369"
    vocab = DatabaseHelper.execute(query)

    return TextParser.kanji_deck_only_main_vocab_word(vocab)

if __name__ == '__main__':
    learned_words = get_learned_rtk_kanji()
    update_cards_to_study_in_database(learned_words)