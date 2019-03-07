'''
This query will return the note data of all cards that you have learned
in the Kanji deck and put the result into 'learned_vocab.txt':

select n.flds
from cards c 
join notes n on c.nid = n.id
where c.type = 2
and c.did = 1543218842369

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
import DatabaseHelper

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

def get_vocab_main():
    '''
    Gets all of the learned Kanji from the results of the query:
    select n.flds
    from cards c 
    join notes n on c.nid = n.id
    where c.type = 2
    '''
    vocab_lst = parse_vocab()
    vocab_lst = get_usable_vocab(vocab_lst)
    with open("learned_vocab_parsed.txt","w+") as f:
        for vocab in vocab_lst:
            f.write(vocab)
            f.write("\n")

def parse_vocab():
    lst = []
    with open("learned_vocab.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            lst.append(line.split("")[4])
    return lst

def get_usable_vocab(lst):
    vlst = []
    for v in lst:
        vlst.append(validate_vocab(v))
    return vlst

def validate_vocab(v):
    if ", " in v:
        v = v.split(", ")[0]
    if "<div>" in v:
        v = v[5:]
    return v

def get_database_filepath():
    with open("db-location.txt", 'r') as f:
        return f.readlines()[0]

if __name__ == '__main__':
    #get_vocab_main()
    #extract_cards_to_study_main()
    print(get_database_filepath())
    db = DatabaseHelper()
    db.test()