import re

import db_actions


def update_compatibility():
    return


def display_companions():

    return


def validate_input(value_type, *prompts):
    while True:
        try:
            for prompt in prompts:
                print(prompt)
                if value_type == 'int':
                    user_input = float(input())
                elif value_type == 'str':
                    user_input = str(input())
                    if (re.search(r'\d', user_input)) is False:
                        return user_input
            break
        except ValueError:
            print("Input must be a number...")


def optimise_garden_layout(my_garden):
    conn, cur = db_actions.connect_to_db()
    for species in my_garden.plants:
        print(species['species_name'])
        companions = cur.execute("SELECT p2, rating FROM Companions WHERE p1 == (?) AND rating >=1 ",
                                 (species['species_name'], ))
        print(companions)
        for companion in companions:
            print(companion)

    return
