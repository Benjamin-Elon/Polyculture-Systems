import db_actions


def update_compatibility():
    return


def get_companions(garden):
    garden_width_m = validate_input("How wide is your garden in meters?\n")
    row_width_m = validate_input("How wide do you want your rows?\n")

    conn, cur = db_actions.connect_to_db()
    cur.execute("SELECT (species_name, crop_type, annual_perrenial, planting_month, harvesting_month,"
                "veg_height_meters, veg_diameter_meters) FROM Species WHERE species_name = (?)", (garden,))
    plants = cur.fetchall()
    print(plants)
    for plant in plants:
        plant_rows = validate_input("Enter desired number of rows for: ", plant['species_name'], "\n")
        plant['num_rows'] = plant_rows

    return


def display_companions():

    return


def validate_input(*prompts):
    while True:
        try:
            for prompt in prompts:
                print(prompt)
                user_input = float(input())
            break
        except ValueError:
            print("Input must be a number...")

    return user_input
