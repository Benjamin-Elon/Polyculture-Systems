import db_actions
import menus
import json
import os


def add_garden():
    conn, cur = db_actions.connect_to_db()
    cur.execute('SELECT species_name FROM Species')
    result = cur.fetchall()
    species_list = []
    x = 0
    for row in result:
        species_list.append(row['species_name'])
        print("(", x, ")", row['species_name'])
        x += 1

    selection = []
    while True:
        x = input("Select a Species to add to garden:")
        if x == '':
            break
        x = int(x)
        if x is not None:
            selection.append(species_list[x])
        elif x not in range(len(species_list)):
            print("Invalid selection...")
        else:
            break

    for x in selection:
        print(x)

    save_garden(selection)
    return


def edit_garden():
    menus.menu("garden_setup")
    return


def remove_garden():
    return


def load_garden():
    print("arrgghh")
    return


def save_garden(garden):
    garden_list = dict()
    filename = "Gardens/gardens"
    if not os.path.exists(filename):
        with open(filename, "w+") as fh:
            fh.close()

    # check if file is emtpy
    with open(filename, "r") as fh:
        data = fh.read()

    # if empty, write garden to file before reading
    if len(data) == 0:
        with open(filename, "w") as fh:
            garden_description = input("Enter a description for this garden:\n")
            garden_list[garden_description] = garden
            json.dump(garden_list, fh)

    # gardens exist
    else:
        # get saved gardens from file
        with open(filename, "r") as fh:
            garden_list = json.load(fh)
            garden_description = input("Enter a description for this garden:\n")
            garden_list[garden_description] = garden
            # print(settings)
            for key, value in garden_list.items():
                print(key, value)

            fh.close()

        # Save the list of gardens to file
        with open(filename, "w") as fh:
            json.dump(garden_list, fh)

    fh.close()

    return