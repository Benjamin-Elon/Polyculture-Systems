import json
import sqlite3

def dict_factory(cursor, row):
    """Causes sqlite to return dictionary instead of tuple"""
    """Easier and more pythonic than using indices"""

    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_table(cur, conn):
    cur.executescript(
    '''
    DROP TABLE IF EXISTS Companions;
    
    CREATE TABLE Companions (
    p1          STRING,
    p2          STRING,
    rating      INTEGER,
    relation_id INTEGER UNIQUE NOT NULL,
    UNIQUE (p1, p2) ON CONFLICT IGNORE
    );
    
    ''')
    return

def connect_to_db():
    conn = sqlite3.connect(r"C:\Users\user\Desktop\Programming\plant_almanac\Syntropy.sqlite")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    print("Done.")
    return conn, cur
    # create_table(cur, conn)
    # conn.commit()

# import companion data to sqlite database
def import_companion_data():

    with open(r"C:\Users\user\Desktop\companions.txt") as fh:
        contents = fh.readlines()
        fh.close()

    contents = contents[0]
    contents = contents.split('[')[1].replace('p1:', '"p1":').replace('p2:', '"p2":').replace('id:', '"id":').replace(
        'b:', '"b":')
    contents = "[" + contents
    contents = json.loads(contents)
    # table = cur.fetchall()

    for item in contents:
        cur.execute('INSERT INTO Companions (p1, p2, rating) VALUES (?,?,?)', (item['p1'], item['p2'], item['b']))
        print(item['p1'], item['p2'], item['b'])
    conn.commit()
    conn.close()

def companion_table_revert():

    cur.execute('SELECT * FROM Companions')
    relations = cur.fetchall()


def check_status(p2, p1_row, rating):
    
    """
    Checks and corrects if there are inconsistencies 
    with companions and incompatibles when importing data
    
    :param p2: str
        name of companion
    :param p1_row: dict 
        species row from database
    :param rating: int
        rating for imported plant relation [-1,0 or 1]
    :return:
    """
    species = p1_row['species_name']

    if rating < 0 and p1_row['known_companions'] is not None and p2 in p1_row['known_companions']:
        p1_row['known_companions'].remove(p2)
        print("removed", p2 , "from", species, 'known_companions')

    elif rating == 0 and p1_row['incompatible_with'] is not None and p2 in p1_row['incompatible_with']:
        p1_row['incompatible_with'].remove(p2)
        print("removed", p2, "from", species, 'incompatible_with')

    elif rating == 0 and p1_row['known_companions'] is not None and p2 in p1_row['known_companions']:
        p1_row['known_companions'].remove(p2)
        print("removed", p2, "from", species, 'known_companions')
    
    # if companion and plant in in incompatible
    elif rating > 1 and p2 in p1_row['incompatible_with']:
        p1_row['incompatible_with'].remove(p2)

    return p1_row


def remove_item():
    return

def convert_to_list(p1_row):
    # print(p1_row['known_companions'])
    # print(p1_row['incompatible_with'])
    # print(type(p1_row['known_companions']))
    # print(type(p1_row['incompatible_with']))
    # print(len(p1_row['known_companions']))
    # print(len(p1_row['incompatible_with']))
    if p1_row['known_companions'] is None:
        p1_row['known_companions'] = []
    elif ',' not in p1_row['known_companions']:
        p1_row['known_companions'] = [p1_row['known_companions']]
    else:
        p1_row['known_companions'] = p1_row['known_companions'].split(',')

    if p1_row['incompatible_with'] is None:
        p1_row['incompatible_with'] = []
    elif ',' not in p1_row['incompatible_with']:
        p1_row['incompatible_with'] = [p1_row['incompatible_with']]
    else:
        p1_row['incompatible_with'] = p1_row['incompatible_with'].split(',')
    print(type(p1_row['known_companions']))
    print(p1_row['incompatible_with'])
    print(len(p1_row['incompatible_with']))

    return p1_row

def companion_table_converter(cur, conn):

    cur.execute('SELECT p1, p2, rating FROM Companions')
    companion_pairs = cur.fetchall()
    print(companion_pairs)
    for pair in companion_pairs:
        p1 = pair['p1']
        p2 = pair['p2']
        rating = pair['rating']
        p1 = p1.replace('_', " ")
        p2 = p2.replace('_', " ")
        if p1 == 'brussels sprouts':
            p1 == 'brussel sprout'
        elif p2 == 'brussels sprouts':
            p2 == 'brussel sprout'

        cur.execute('SELECT * FROM Species WHERE species_name == (?)', (p1,))
        p1_row = cur.fetchone()

        print('comparing', p1, p2)
        print("p1row:", p1_row)

        # Add species to database if it doesn't already exist
        if p1_row is None:
            print('111111')
            cur.execute('INSERT OR IGNORE INTO Species (species_name) VALUES (?)', (p1,))
            p1_row = {'species_name': p1, 'known_companions': [], 'incompatible_with': []}
            conn.commit()

        print(p1_row['known_companions'], p1_row['incompatible_with'])
        p1_row = convert_to_list(p1_row)

        # if there is no rating
        if rating in ["",None]:
            continue

        # verify no mistakes were made previously
        p1_row = check_status(pair['p2'], p1_row, pair['rating'])

        # incompatible
        if rating < 0:
            try:
                if p2 not in p1_row['incompatible_with']:
                    p1_row['incompatible_with'].append(p2)
                    cur.execute('UPDATE Species SET incompatible_with == (?) WHERE species_name == (?) ',
                                (','.join(p1_row['incompatible_with']), p1))
            except TypeError:
                cur.execute('UPDATE Species SET incompatible_with == (?) WHERE species_name == (?) ', (p2, p1))

        elif rating > 0:
            try:
                if p2 not in p1_row['known_companions']:
                    p1_row['known_companions'].append(p2)
                    cur.execute('UPDATE Species SET known_companions == (?) WHERE species_name == (?) ',
                                (','.join(p1_row['known_companions']), p1))
            except TypeError:
                cur.execute('UPDATE Species SET known_companions == (?) WHERE species_name == (?) ',
                            (p2, p1))
        conn.commit()


conn,cur = connect_to_db()
companion_table_converter(cur, conn)

# import_companion_data()