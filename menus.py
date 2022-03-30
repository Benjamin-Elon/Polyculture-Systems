import garden_setup
import companion_planter
import task_scheduler

menus = \
    {"garden_select": {"prompt": "Would you like to:",
                       "options": [["Use existing garden", garden_setup.load_garden],
                                   ["Edit gardens", garden_setup.edit_garden],
                                   ["Update plant compatibility ratings", companion_planter.update_compatibility]]},

     "main": {"prompt": "Would you like to:",
              "options": [["Get companion recommendations", companion_planter.reccomend_companions()],
                          ["Show active gardening tasks", task_scheduler.show_tasks]]},

     "garden_setup": {"prompt": "Would you like to:",
                      "options": [["New garden (Create a list of plants)", garden_setup.add_garden],
                                  ["Remove garden (Remove a list of plants)", garden_setup.remove_garden],
                                  ["Edit garden (Edit a list of plants)", garden_setup.edit_garden]]}
     }


def menu(menu_key):
    menu_items = menus[menu_key]
    print(menu_items["prompt"], "\n")
    for x in range(len(menu_items["options"])):
        print("(", x, ") ", menu_items["options"][x][0])

    x = int(input())
    menu_items["options"][x][1]()
    return
