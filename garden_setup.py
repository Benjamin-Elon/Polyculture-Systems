import tools
import db_actions
import menus
import json
import os
import python_weather


class Garden:
    def __init__(self):
        self.location = None
        self.plants = None
        self.garden_width = None
        self.row_width = None
        self.path_width = None
        self.intensity_spacing = None
        self.configuration = None
        self.garden_layout = None


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

    save_file(selection, "gardens")
    return


def edit_garden():
    menus.menu("garden_setup", 'gardens')
    return


def load_garden(file_type, location=None):
    print(file_type)
    filename = "Gardens/" + file_type

    if not os.path.exists(filename):
        with open(filename, "w+") as fh:
            fh.close()

    with open(filename, 'r') as fh:
        contents = fh.readlines()
        fh.close()

    if contents:
        if file_type == "gardens":
            with open(filename, 'r') as fh:
                files = json.load(fh)
            menu = []
            x = 0
            for file in files:
                print("(", x, ")", file)
                x += 1
                menu.append(files[file])
            print("(", x + 5, ") Delete a garden")

            while True:
                try:
                    choice = int(input("Select an garden to load:\n"))
                    if choice == x + 5:
                        x = int(input("Select garden to delete:\n"))
                        del menu[x]
                        if len(menu) == 1:
                            print("No more gardens")
                            return None
                        x = 0
                        for file in menu:
                            print("(", x, ")", file)
                            x += 1
                        print("(", x + 5, ") Delete a garden")
                        continue
                    garden = menu[choice]

                    return menus.menu('garden_actions', garden)
                except (ValueError, IndexError):
                    print("Invalid selection.")

    else:
        print("No gardens saved.")
        return None


def save_file(file_data, file_type, location=None):
    file_list = dict()
    filename = "Gardens/" + file_type
    if not os.path.exists(filename):
        with open(filename, "w+") as fh:
            fh.close()

    # check if file is emtpy
    with open(filename, "r") as fh:
        data = fh.read()

    # if empty, write garden to file before reading
    if file_type == "garden":
        if len(data) == 0:
            with open(filename, "w") as fh:
                description = input("Enter a description for this garden:\n")
                file_list[description] = file_data
                json.dump(file_list, fh)

    # gardens exist
    else:
        # get saved gardens from file
        with open(filename, "r") as fh:
            file_list = json.load(fh)
            if file_type == "garden":
                description = input("Enter a description for this garden:\n")
            elif file_type == "weather":
                description = location
            file_list[description] = file_data
            # print(settings)
            for key, value in file_list.items():
                print(key, value)

            fh.close()

        # Save the list of gardens to file
        with open(filename, "w") as fh:
            json.dump(file_list, fh)

    fh.close()

    return


def validate_location(location):

    return location


def configure_garden(plant_list):
    my_garden = Garden()
    location = tools.validate_input("Input a location for your garden (closest city)")
    my_garden.location = validate_location(location)
    my_garden.garden_width = tools.validate_input("int", "How wide is your garden in meters?\n")
    my_garden.row_width = tools.validate_input("int", "How wide do you want your rows?\n")
    my_garden.path_width = tools.validate_input("int", "How wide would you like your paths?")
    plants = []
    conn, cur = db_actions.connect_to_db()
    for plant in plant_list:
        cur.execute("SELECT species_name, crop_type, annual_perrenial, planting_month, harvesting_month, "
                    "veg_height_meters, veg_diameter_meters FROM Species WHERE species_name = (?)", (plant,))
        plant = cur.fetchall()
        plants.append(plant[0])

    for x in range(len(plants)):
        print(plants[x])
        plant_rows = tools.validate_input("int", "Enter desired number of rows for: " + plants[x]['species_name'] + "\n")
        plants[x]['num_rows'] = plant_rows
    my_garden.plants = plants
    print(my_garden.plants)
    my_garden.garden_layout = tools.optimise_garden_layout(my_garden)

    return

