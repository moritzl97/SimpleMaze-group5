# This file contains all functions of the dragon room.
# Scroll down to the main function enterDragon Room() which is called when the dragon room is entered.

import random
import time

#---define open dialog---#
# Called if player talks to an NPC or interacts with objects
def open_dialog(npc, state):
    # Loop through all dialog nodes in the current chapter. Ends if the chapter is finished
    while True:
        #get current dialog node by looking up the current chapter and node for the npc
        node = npc["dialog_tree"][npc["current_chapter"]][npc["current_node"]]

        # Print dialog text
        print(f"{node['text']}")

        # Call function if there is an action defined at this point in the dialog
        if "action" in node:
            #lookup the function that should be called from the dialog
            actions = node["action"]
            if type(actions) != list:
                # Make a list of it, if it is not a list
                actions = [actions]
            for action, argument in actions: # loop over the list
                if action  == "wait":
                    wait(argument, state)
                elif action == "add_npc":
                    add_npc(argument, state)
                elif action == "give_item":
                    give_item(argument, state)
                elif action == "remove_object":
                    remove_object(argument, state)
                elif action == "add_item":
                    add_item(argument, state)
                elif action == "make_dragon_angry":
                    make_dragon_angry(argument, state)
                elif action == "try_remove_item_from_inv":
                    try_remove_item_from_inv(argument, state)
                elif action == "remove_npc":
                    remove_npc(argument, state)

        # If there are no branching dialog options end dialog
        if "next_chapter" in node:
            #Save the next chapter to the npc
            npc["current_chapter"] = node["next_chapter"]
            npc["current_node"] = "start"
            return

        # If there are options print all of them
        print("\nChoices:")
        for option_number, option_entry in node["options"].items():
            # Calculate success rate and see if helpful items are in the players inventory
            success_rate = option_entry["base_success_rate"]
            added_modifier_list = []
            for item, modifier in option_entry.get("success_modifiers", {}).items():
                if item in state["inventory"]:
                    success_rate += modifier
                    added_modifier_list.append(item)

            # Cap success rate if to many bonuses were added
            if success_rate > 1:
                success_rate = 1

            # Print option number, the text and the success rate if you choose this option
            print(f" {option_number}. {option_entry['text']} ({int(success_rate*100)}%) ")
            # If there are items that helped, list them
            if added_modifier_list:
                print(f"Helping items: {', '.join(added_modifier_list)}")

        leave_option = str(len(node["options"]) + 1)
        print(f" {leave_option}. Leave")

        # Input loop
        # Checks if the player entered a valid option
        while True:
            choice = input("\n> ").strip()
            # Check if player selected leave option
            if choice == leave_option:
                print("You back of to do something else.")
                return
            # If choice is in options check for success, else ask again for an input
            elif choice not in node["options"]:
                print("Please choose a valid option.")
                continue
            else:
                # If valid choice, calculate the success rate again
                option_entry = node["options"][choice]
                success_rate = option_entry["base_success_rate"]
                for item, modifier in option_entry.get("success_modifiers", {}).items():
                    if item in state["inventory"]:
                        success_rate += modifier
                if success_rate > 1:
                    success_rate = 1
                # Roll the dice and see if successful or failure:
                if success_rate > random.uniform(0, 1):
                    npc["current_node"] = option_entry["next_success"] # set the next dialog to success
                    print("\033[32mSuccess!\033[0m") #The wired stuff \033[32m and \033[0m makes the text green
                else:
                    npc["current_node"] = option_entry["next_failure"] # set the next dialog to failure
                    print("\033[31mFailure!\033[0m") #The wired stuff \033[31m and \033[0m makes the text red
                break # go back to the first loop and print the next dialog node
#---end talk definition---#

#---define shop keeper---#
def trade_with_shopkeeper(npc, state):
    #Get items that the shopkeeper wants to trade
    items_sell = npc["items_for_sale"]
    wanted_items = npc["wanted_items"]

    if not items_sell:
        print("I have nothing to trade anymore.")
        return

    print("I will trade the following items with you:")
    while True:
        number_of_options = len(items_sell)+1
        for index in range(1, number_of_options):
            print(f"{index}. {items_sell[index-1]} for {wanted_items[index-1]}")
        print(f"{number_of_options}. I don't want to trade.")

        choice = int(input("\n> ").strip())

        if choice < number_of_options:
            # if correct input
            item_sell = items_sell[choice-1]
            item_wanted = wanted_items[choice-1]
            # Check if the player really has the item that he want to give the shopkeeper in the inventory
            if item_wanted in state["inventory"]:
                state["inventory"].remove(item_wanted)
                state["inventory"].append(item_sell)
                items_sell.pop(choice-1)
                wanted_items.pop(choice-1)
                print("Thank you for the trade.")
                return
            else:
                print(f"Do you want to swindle me? You don't have {item_wanted} in your inventory!")
                continue
        elif choice == number_of_options:
            # Leave and dont trade
            print("Maybe next time we can make a deal.")
            return
        else:
            print("Please choose a valid option.")
#---end of shopkeeper---#

#---Action functions---#
# Functions that change the room if the player makes choices. Called when something in the dialog happens.
def wait(seconds, state):
    # Wait for input seconds
    for i in range(seconds, 0, -1):
        # print the whole line each time, start with \r to return to line start
        print(f"\rYou are stunned for {i} seconds.  ", end='', flush=True)
        time.sleep(1)
    print("\nYou shake it off and can act again.")

def add_npc(argument, state):
    # Adds npc to the room
    if argument == "Shopkeeper":
        state["dragon_room"]["npcs"]["Shopkeeper"] = {"items_for_sale": ["Broadsword","Sneaking-Boots","Lockpick"], "wanted_items": ["Gemstone","Chalk","Pickaxe"]}
    elif argument == "Fairy":
        from .dragon_room_dialog import dialogue_tree_fairy
        state["dragon_room"]["npcs"]["Fairy"] = {"current_chapter":"first_chapter", "current_node":"start", "dialog_tree":dialogue_tree_fairy}
    elif argument == "Kobold":
        from .dragon_room_dialog import dialogue_tree_kobold
        state["dragon_room"]["npcs"]["Kobold"] = {"current_chapter":"first_chapter", "current_node":"start", "dialog_tree":dialogue_tree_kobold}
    elif argument == "Dragon":
        from .dragon_room_dialog import dialogue_tree_dragon
        state["dragon_room"]["npcs"]["Dragon"] = {"current_chapter": "first_chapter", "current_node": "start", "dialog_tree": dialogue_tree_dragon}

def add_item(argument, state):
    #Adds item to the room
    state["dragon_room"]["items"].append(argument)

def give_item(argument, state):
    #Adds item to players inventory
    if not argument in state["inventory"]:
        state["inventory"].append(argument)

def remove_object(argument, state):
    # Remove object from room
    state["dragon_room"]["interactable_objects"].pop(argument)

def remove_npc(argument, state):
    #Remove npc from room
    state["dragon_room"]["npcs"].pop(argument)

def try_remove_item_from_inv(argument, state):
    # Remove item from inventory, if it is in the inventory
    if argument in state["inventory"]:
        state["inventory"].pop(argument)

def make_dragon_angry(argument, state):
    # Sets the next dialog of the dragon to angry
    if "Dragon" in state["dragon_room"]["npcs"]:
        state["dragon_room"]["npcs"]["Dragon"]["current_chapter"] = "dragon_angry"
        state["dragon_room"]["npcs"]["Dragon"]["current_node"] = "start"
#---End of action functions---#

#---Command handlers---#
def handle_look(noun, state):
    if noun:
        # States where the given noun is (if in the room)
        if noun in state["dragon_room"]["items"]:
            print(f"You look at the {noun}. It might be useful if you pick it up.")
        elif noun in state["dragon_room"]["npcs"]:
            print(f"You look at the {noun}. You can talk to them if you want to.")
        elif noun in state["dragon_room"]["interactable_objects"]:
            open_dialog(state["dragon_room"]["interactable_objects"][noun], state)
        elif noun in state["inventory"]:
            print(f"You find {noun} in your inventory.")
        else:
            print(f"You don't see a {noun} here.")
    else:
        #Prints a description of the room and lists all things that are in the room
        print("You are in a classroom with a huge hole in the ground. You see smoke rising from the hole.\n"
              "The chairs and desks of the students are scatterd through the room.\n"
              "Only the teachers desk is still standing on its right place.\n"
              "On the blackboard is something written, but it is to small to read from here.\n")
        if state["dragon_room"]['items']:
            print(f"You see the following items in the room: {', '.join(state['dragon_room']['items'])}")
        if state["dragon_room"]['npcs']:
            print(f"You can talk to the following NPCs in the room: {', '.join(state['dragon_room']['npcs'].keys())}")
        if state["dragon_room"]['interactable_objects']:
            print(f"You see these points of interest in the room: {', '.join(state['dragon_room']['interactable_objects'].keys())}")
    return

def handle_take(noun, state):
    #Pick up item and add it to inventory
    if not noun:
        print("Take what?")
    elif noun in state["inventory"]:
        print(f"You already have the {noun} in your inventory.")
    elif noun in state["dragon_room"]["items"]:
        state["dragon_room"]["items"].remove(noun)
        state["inventory"].append(noun)
        print(f"You take {noun}.")
    else:
        print(f"You cannot pickup {noun}.")
    return

def handle_trade(noun, state):
    # opens trade menu with the shopkeeper
    if "Shopkeeper" in state["dragon_room"]["npcs"]:
        trade_with_shopkeeper(state["dragon_room"]["npcs"]["Shopkeeper"], state)
    else:
        print("There is nobody to trade with here.")
    return

def handle_interact(noun, state):
    # opens dialog with an object or a npc
    if not noun:
        print("Interact with what?")
    else:
        if noun in state["dragon_room"]["interactable_objects"]:
            open_dialog(state["dragon_room"]["interactable_objects"][noun], state)
        elif noun in noun in state["dragon_room"]["npcs"]:
            if noun == "Shopkeeper":
                trade_with_shopkeeper(state["dragon_room"]["npcs"]["Shopkeeper"], state)
            else:
                #Print ASCII art if you talk with dragon
                if noun == "Dragon":
                    print(r"""                                              /(  /(
                                            /   \/   \
                              |\___/|      //||\//|| \\
                             (,\  /,)\__  // ||// || \\ \
                             /     /   /_//  |//  ||  \\ \\
                            (@_^_@)/    /_   //   ||   \\  \\
                             W//W_/      /_ //    ||    \\   \\
                           (//) |         ///     ||     \\    \\
                         (/ /) _|_ /   )  //      ||      \\   __\
                       (// /) '/,_ _ _/  ( ; -.   ||    _ _\\.-~        .-~~~^-.
                     (( // )) ,-{        _      `-||.-~-.           .~         `.
                    (( /// ))  '/\      /                 ~-. _ .-~      .-~^-.  \
                    (( ///))      `.   {            }                   /      \  \
                     ((/ ))     .----~-.\        \-'                 .~         \  `. \^-.
                               ///.----..>    (   \             _ -~             `.  ^-`   ^-_
                                 ///-._ _ _ _ _ _ _}^ - - - - ~                    ~--_.   .-~
                                                                                       /.-~""")

                open_dialog(state["dragon_room"]["npcs"][noun], state)
        else:
            print(f"There is no {noun} here to interact with.")
    return

def handle_help(noun, state):
    # list commands
    print("Type in a verb and a noun to interact with the things in the room.\nType 'look around' to see what is in the room. \nUse verbs lik: 'look', 'talk', 'inspect', 'trade'")

# ---Parser---#
def parse(user_input):
    # transforms input of the user into verb and a noun. Synonyms of verbs are converted into known commands. Removes unnecessary words like "the", "to", "with".

    # Transform input string into a list
    words = user_input.lower().split()
    # Remove unnecessary words
    fluff = {"the", "a", "an", "to", "up", "with", "around"}
    words = [word for word in words if word not in fluff]

    if not words:
        return None, None

    # First word is assumed to be the verb
    verb = words[0]
    noun = None
    # synonym list of verbs
    verb_aliases = {
        "inspect": "look",
        "examine": "look",
        "explore": "look",
        "pick": "take",
        "grab": "take",
        "collect": "take",
        "fetch": "take",
        "sell": "trade",
        "buy": "trade",
        "barter": "trade",
        "use": "interact",
        "talk": "interact",
        "speak": "interact",
        "converse": "interact",
        "chat": "interact",
        "communicate": "interact",
        "?": "help"
    }
    # Get command for synonyms of verb
    if verb in verb_aliases.keys():
        verb = verb_aliases[verb]

    # Define the noun as the second word
    if len(words) > 1:
        noun = words[1].title()

    return verb, noun
# ---Parser end---#

#---Main functions---#
# Called when dragon room is entered
def dragon_room_enter(state):
    # If player has finished the dragon room print this message and return them to the corridor
    if state["visited"]["dragon_room"]:
        print("You have already dealt with the dragon and are ready to move to another room.")
        return False

    #---setup room---#
    # initialize room state: everything what is in the room is stored here
    state["dragon_room"] = {"items":[], "interactable_objects":{}, "npcs":{}}

    # import the dialog tree from the dragon_room_dialog.py file and create objects starting in the room
    from .dragon_room_dialog import dialogue_tree_cracked_wall, dialogue_tree_blackboard, dialogue_tree_desk, dialogue_tree_chest, dialogue_tree_hole
    state["dragon_room"]["interactable_objects"]["Cracked-Wall"] = {"current_chapter":"first_chapter", "current_node":"start", "dialog_tree":dialogue_tree_cracked_wall}
    state["dragon_room"]["interactable_objects"]["Blackboard"] = {"current_chapter": "first_chapter", "current_node": "start", "dialog_tree": dialogue_tree_blackboard}
    state["dragon_room"]["interactable_objects"]["Desk"] = {"current_chapter": "first_chapter", "current_node": "start", "dialog_tree": dialogue_tree_desk}
    state["dragon_room"]["interactable_objects"]["Chest"] = {"current_chapter": "first_chapter", "current_node": "start","dialog_tree": dialogue_tree_chest}
    state["dragon_room"]["interactable_objects"]["Hole"] = {"current_chapter": "first_chapter", "current_node": "start", "dialog_tree": dialogue_tree_hole}
    state["dragon_room"]["items"].append("Pickaxe")
    #---room setup finished---#

    # start room
    print("You enter the classroom and are immediately drawn to the huge hole in the ground.You see smoke rising from the hole.\n"
          "The chairs and desks of the students are scatterd through the room.\n"
          "Only the teachers desk is still standing on its right place.\n"
          "On the blackboard is something written, but it is to small to read from here.")
    return True

# Dragon room custom commands
def dragon_room_commands(command, state):
    # transforms input of the user into verb and a noun. Synonyms of verbs are converted into known commands. Removes unnecessary words like "the", "to", "with".
    verb, noun = parse(command)

    if verb == "look":
        handle_look(noun, state)
        return True
    elif verb == "take":
        handle_take(noun, state)
        return True
    elif verb == "trade":
        handle_trade(noun, state)
        return True
    elif verb == "interact":
        handle_interact(noun, state)
        return True
    elif verb == "help":
        handle_help(noun, state)
        return True

    if "Trophy" in state["inventory"]:
        print("You have successfully dealt with the dragon. You can now move on to another room.")
        state["visited"]["dragon_room"] = True

    return False
