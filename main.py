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

def extract_cards_to_study_main():
    '''
    Gets all of the Sort ID's for the cards that contain
    only the vocabulary that you have learned. Then it 
    generates a query which will update all of the cards
    that you need to learn by un-suspending them and setting
    them to 'New'. The query is as follows:
    update cards
    set queue = 0, type = 0
    where nid in
    (
    select id
    from notes
    where sfld in (x,y,z)
    )
    and did = 1547537208241
    '''
    studied_vocab = []
    with open("learned_vocab_parsed.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            studied_vocab.append(line)

    studied_vocab = "\n".join(studied_vocab).split("\n")[::2]

    id_lst = []
    with open("japanese.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.split("\t")[4].split(", ") == ['']:
                continue
            if set(line.split("\t")[4].split(", ")).issubset(studied_vocab):
                id_lst.append(line.split("\t")[1])

    unlearned_ids = []
    with open("unlearned_vocab.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            unlearned_ids.append(line)

    unlearned_ids = "\n".join(unlearned_ids).split("\n")[::2]

    final_id_lst = []
    for n in id_lst:
        if n in unlearned_ids:
            final_id_lst.append(n)

    output = "update cards\n"
    output += "set queue = 0, type = 0\n"
    output += "where nid in \n"
    output += "(\n"
    output += "select id \n"
    output += "from notes \n"
    output += "where sfld in (" + ", ".join(final_id_lst) + ")\n"
    output += ")\n"
    output += "and did = 1547537208241"

    print(output)

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
    vocab = DatabaseHelper.execute(__get_database_filepath(), query)
    return TextParser.kanji_deck_only_main_vocab_word(vocab)

def __get_database_filepath():
    with open("db-location.txt", 'r') as f:
        return f.readlines()[0]

if __name__ == '__main__':
    #get_learned_rtk_kanji()
    #extract_cards_to_study_main()
    for vocab in get_learned_rtk_kanji():
        print(vocab)