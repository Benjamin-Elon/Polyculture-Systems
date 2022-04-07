import re
import db_actions


def update_compatibility():
    return


def display_companions():
    return


def optimise_garden_layout(my_garden):
    conn, cur = db_actions.connect_to_db()
    for species in my_garden.plants:
        print(species['species_name'])
        results = cur.execute("SELECT p2, rating FROM Companions WHERE p1 == (?) AND rating >=1 ",
                                     (species['species_name'],))
        companion_list = cur.fetchall()
        for plants in companion_list:
            print(plants.keys())
            # print(plants['p2'])

    return
