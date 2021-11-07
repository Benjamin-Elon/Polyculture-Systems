import sqlite3


# def dict_factory(cursor, row):
#     """Causes sqlite to return dictionary instead of tuple"""
#     """Easier and more pythonic than using indices"""
#
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#     return d

def open_database():
    conn = sqlite3.connect(r"C:\Users\user\Desktop\Programming\plant_almanac\Syntropy.sqlite")
    # conn.row_factory = dict_factory
    cur = conn.cursor()
    print("Done.")
    return cur,conn

def close_database(conn):
    """Closes the database"""
    conn.close()
    return

def find_companions(cur):
    cur.execute('SELECT variety_name FROM Species')
    species = cur.fetchall()

    x = 0
    species_menu = list()
    for item in species:
        species_menu.append(item[0])
        x += 1
    selection = species_select(species_menu)
    recommender(selection, cur)
    return


def species_select(species_menu):

    species_menu = list(enumerate(species_menu))
    for [num, name] in species_menu:
        print('(' + str(num) + ')', name)

    print("Select species you are planting:\n"
          "When finished, press 'Enter' to continue")
    selection = []
    while True:

        x = input()

        if x == '' and selection == []:
            print("make a selection.\n")
        elif x == '':
            break

        # if valid selection, add it to the list
        else:
            try:
                x = int(x)
                name = species_menu[x]
            except (ValueError, KeyError, IndexError):
                print("invalid selection...")
            else:
                if name in selection:
                    print("already selected...")
                else:
                    sselection = selection.append(name[1])
    print(selection)
    return selection

def companion_completor():
    return

def recommender(selection, cur):

    for i in range(len(selection)):
        selection[i] = selection[i].lower()

    for species in selection:
        cur.execute('SELECT known_companions FROM Species WHERE (variety_name) IS (?)', (species,))
        companions = cur.fetchone()[0]

        try:
            companions = companions.split(',')
        except (AttributeError):
            print(species, "has no companions")
            continue

        for i in range(len(companions)):
            companions[i] = companions[i].lower().strip()

        for companion in companions:
            if companion in selection:
                print(species, companion)
        # if species in comapnions:
        #     print(species,comapnions)

