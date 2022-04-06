import garden_setup
import companion_planter
import task_scheduler

menus = \
    {"select_garden": {"prompt": "Would you like to:",
                       "options": [["Use existing garden", garden_setup.load_garden],
                                   ["Edit gardens", garden_setup.edit_garden]]},

     "garden_actions": {"prompt": "Would you like to:",
                        "options": [["Get companion recommendations", garden_setup.configure_garden],
                                    ["Show active gardening tasks", task_scheduler.show_tasks]]},

     "garden_setup": {"prompt": "Would you like to:",
                      "options": [["New garden (Create a list of plants)", garden_setup.add_garden],
                                  ["Remove garden (Remove a list of plants)", garden_setup.edit_garden],
                                  ["Edit garden (Edit a list of plants)", garden_setup.edit_garden]]}
     }


# displays a menu based on dictionary of menu options
def menu(menu_key, *params):
    if len(params) == 1:
        params = params[0]
    # fetch menu
    menu_items = menus[menu_key]
    print(menu_items["prompt"], "\n")
    # print options
    for x in range(len(menu_items["options"])):
        print("(", x, ") ", menu_items["options"][x][0])

    while True:
        try:
            x = int(input())
            break
        except ValueError:
            print("Input must be a number...")

    # call function based on menu selection, along with any parameters (i.e. garden config)
    print(params)
    if params == ():
        menu_items["options"][x][1]()
    else:
        menu_items["options"][x][1](params)
    return
