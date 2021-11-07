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


conn,cur = connect_to_db()
# import_companion_data()
cur.execute('SELECT p1, p2, rating FROM Companions')
companion_pairs = cur.fetchall()
print(companion_pairs)
for pair in companion_pairs:

    p1 = pair['p1']
    p2 = pair['p2']
    print(p1,p2)
    cur.execute('SELECT * FROM Species WHERE variety_name == (?)', (p1,))
    p1_row = cur.fetchone()
    cur.execute('SELECT * FROM Species WHERE variety_name == (?)', (p2,))
    p2_row = cur.fetchone()
    print("p1row:", p1_row)

    if p1_row is None:
        cur.execute('INSERT OR IGNORE INTO Species (variety_name) VALUES (?)', (p1,))
    if p2_row is None:
        cur.execute('INSERT OR IGNORE INTO Species (variety_name) VALUES (?)', (p2,))
    conn.commit()

    # if there is no rating
    if pair['rating'] in ["",None]:
        continue
    else:
        if p1_row['known_companions'] is None:
            cur.execute("INSERT OR IGNORE INTO Species (known_companions) WHERE variety_name == (?)",(p2))
        if p2 not in p1_row['known_companions']:
            print(row['known_companions'])
    elif pair['rating'] < 0:
        continue
    elif pair['rating'] == 0:
        continue
