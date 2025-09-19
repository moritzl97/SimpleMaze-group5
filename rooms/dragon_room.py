import random
import time
import sys

#---define open dialog---#
# Called if player talks to an NPC or interacts with objects
def open_dialog(npc, room_state):
    # If a dialog option causes something to happen, the function is looked up in this table
    action_map = {
        "wait": wait,
        "add_npc": add_npc,
        "give_item": give_item,
        "remove_object": remove_object,
        "add_item": add_item,
        "make_dragon_angry" : make_dragon_angry,
        "remove_item": remove_item,
        "remove_npc": remove_npc
    }

    # Loop through all dialog nodes in the current chapter. Ends if the chapter is finished
    while True:
        #get current dialog node by looking up the current chapter and node for the npc
        node = npc["dialog_tree"][npc["current_chapter"]][npc["current_node"]]

        # Print dialog text
        print(f"{node['text']}")

        # Run action if defined. When in a list execute all actions. If not wrap action in list.
        if "action" in node:
            actions = node["action"]
            if type(actions) != list:
                actions = [actions]
            for executable_action in actions:
                function, argument = executable_action
                function = action_map.get(function)
                function(argument, room_state)

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
                if item in room_state["inventory"]:
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
                option_entry = node["options"][choice]
                success_rate = option_entry["base_success_rate"]

                for item, modifier in option_entry.get("success_modifiers", {}).items():
                    if item in room_state["inventory"]:
                        success_rate += modifier

                if success_rate > 1:
                    success_rate = 1

                if success_rate > random.uniform(0, 1):
                    npc["current_node"] = option_entry["next_success"]
                    print("\033[32mSuccess!\033[0m") #The wired stuff \033[32m and \033[0m makes the text green
                else:
                    npc["current_node"] = option_entry["next_failure"]
                    print("\033[31mFailure!\033[0m") #The wired stuff \033[31m and \033[0m makes the text red
                break
#---end talk definition---#

#---define shop keeper---#
def trade_with_shopkeeper(npc, room_state):
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
        # If choice is in options check for success, else ask again for an input
        if choice < number_of_options:
            item_sell = items_sell[choice-1]
            item_wanted = wanted_items[choice-1]

            if item_wanted in room_state["inventory"]:
                room_state["inventory"].remove(item_wanted)
                room_state["inventory"].append(item_sell)
                items_sell.pop(choice-1)
                wanted_items.pop(choice-1)
                print("Thank you for the trade.")
                return
            else:
                print(f"Do you want to swindle me? You don't have {item_wanted} in your inventory!")
                continue
        elif choice == number_of_options:
            print("Maybe next time we can make a deal.")
            return
        else:
            print("Please choose a valid option.")
#---end of shopkeeper---#

#---Parser---#
def parse(user_input):
    #Transform input string into a list
    words = user_input.lower().split()

    #Remove unnecessary words
    fluff = {"the", "a", "an", "to", "up", "with", "around"}
    words = [word for word in words if word not in fluff]

    if not words:
        return None, None

    verb = words[0]
    noun = None

    verb_aliases = {
        "inspect": "look",
        "examine": "look",
        "explore": "look",
        "inv": "inventory",
        "pick": "take",
        "grab": "take",
        "collect": "take",
        "fetch": "take",
        "walk": "go",
        "move": "go",
        "leave": "go",
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

    if verb in verb_aliases.keys():
        verb = verb_aliases[verb]

    if len(words) > 1:
        noun = words[1].title()

    return verb, noun
#---Parser end---#

#---Action functions---#
# Functions that change the room if the player makes choices
def wait(seconds, room_state):
    for i in range(seconds, 0, -1):
        # print the whole line each time, start with \r to return to line start
        print(f"\rYou are stunned for {i} seconds.  ", end='', flush=True)
        time.sleep(1)
    print("\nYou shake it off and can act again.")

def add_npc(argument, room_state):
    if argument == "Shopkeeper":
        room_state["npcs"]["Shopkeeper"] = {"items_for_sale": ["Broadsword","Sneaking-Boots","Lockpick"], "wanted_items": ["Gemstone","Chalk","Pickaxe"]}
    elif argument == "Fairy":
        from .dragon_room_dialog import dialogue_tree_fairy
        room_state["npcs"]["Fairy"] = {"current_chapter":"first_encounter", "current_node":"start", "dialog_tree":dialogue_tree_fairy}
    elif argument == "Kobold":
        from .dragon_room_dialog import dialogue_tree_kobold
        room_state["npcs"]["Kobold"] = {"current_chapter":"first_encounter", "current_node":"start", "dialog_tree":dialogue_tree_kobold}
    elif argument == "Dragon":
        from .dragon_room_dialog import dialogue_tree_dragon
        room_state["npcs"]["Dragon"] = {"current_chapter": "first_encounter", "current_node": "start", "dialog_tree": dialogue_tree_dragon}

def add_item(argument, room_state):
    room_state["items"].append(argument)

def give_item(argument, room_state):
    if not argument in room_state["inventory"]:
        room_state["inventory"].append(argument)

def remove_item(argument, room_state):
    if argument in room_state["inventory"]:
        room_state["inventory"].remove(argument)

def remove_object(argument, room_state):
    room_state["interactable_objects"].pop(argument)

def remove_npc(argument, room_state):
    room_state["npcs"].pop(argument)

def make_dragon_angry(argument, room_state):
    if "Dragon" in room_state["npcs"]:
        room_state["npcs"]["Dragon"]["current_chapter"] = "dragon_angry"
        room_state["npcs"]["Dragon"]["current_node"] = "start"
#---End of action functions---#

#---Command handlers---#
def handle_look(noun, room_state):
    if noun:
        if noun in room_state["items"]:
            print(f"You look at the {noun}. It might be useful if you pick it up.")
        elif noun in room_state["npcs"]:
            print(f"You look at the {noun}. You can talk to them if you want to.")
        elif noun in room_state["interactable_objects"]:
            open_dialog(room_state["interactable_objects"][noun], room_state)
        elif noun in room_state["inventory"]:
            print(f"You find {noun} in your inventory.")
        else:
            print(f"You don't see a {noun} here.")
    else:
        print("You are in a classroom with a huge hole in the ground. You see smoke rising from the hole.\n"
              "The chairs and desks of the students are scatterd through the room.\n"
              "Only the teachers desk is still standing on its right place.\n"
              "On the blackboard is something written, but it is to small to read from here.\n")
        if room_state['items']:
            print(f"You see the following items in the room: {', '.join(room_state['items'])}")
        if room_state['npcs']:
            print(f"You can talk to the following NPCs in the room: {', '.join(room_state['npcs'].keys())}")
        if room_state['interactable_objects']:
            print(f"You see these points of interest in the room: {', '.join(room_state['interactable_objects'].keys())}")
    return True

def handle_go(noun, room_state):
    if not noun:
        print("Go to which room?")
    elif noun.lower() in ["corridor", "back", "room", "dragonroom"]:
        print("You flee the dragon room.")
        return False
    elif noun in room_state["interactable_objects"]:
        handle_interact(noun, room_state)
        return True
    else:
        print(f"You can't go to '{noun}' from here.")
    return True

def handle_take(noun, room_state):
    if not noun:
        print("Take what?")
    elif noun in room_state["inventory"]:
        print(f"You already have the {noun} in your inventory.")
    elif noun in room_state["items"]:
        room_state["items"].remove(noun)
        room_state["inventory"].append(noun)
        print(f"You take {noun}.")
    else:
        print(f"You cannot pickup {noun}.")
    return True

def handle_trade(noun, room_state):
    if "Shopkeeper" in room_state["npcs"]:
        trade_with_shopkeeper(room_state["npcs"]["Shopkeeper"], room_state)
    else:
        print("There is nobody to trade with here.")
    return True

def handle_interact(noun, room_state):
    if not noun:
        print("Interact with what?")
    else:
        if noun in room_state["interactable_objects"]:
            open_dialog(room_state["interactable_objects"][noun], room_state)
        elif noun in noun in room_state["npcs"]:
            if noun == "Shopkeeper":
                trade_with_shopkeeper(room_state["npcs"]["Shopkeeper"], room_state)
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

                open_dialog(room_state["npcs"][noun], room_state)
        else:
            print(f"There is no {noun} here to interact with.")
    return True

def handle_inventory(noun, room_state):
    if room_state["inventory"]:
        print("You are carrying:")
        for item in room_state["inventory"]:
            print(f" - {item}")
    else:
        print("You are not carrying anything.")
    return True

def handle_help(noun, room_state):
    print("Type in a verb and a noun to interact with the things in the room.\nType 'look around' to see what is in the room. You can leave the room by typing: 'go corridor'.\nUse 'inventory' to look in your inventory.\nUse verbs lik: 'look', 'talk', 'inspect', 'trade'")
    return True

def handle_quit(noun, room_state):
    print("👋 You leave the school and the adventure comes to an end. Game over.")
    sys.exit()
#---Command handlers finished---#

#---Main function---#
# Called when dragon room is entered
def enterDragonRoom(state):

    if state["visited"]["dragonroom"]:
        print("You have already dealt with the dragon and are ready to move to another room.")
        return "corridor"

    # dict to store command handler functions
    commands = {
        "go": handle_go,
        "take": handle_take,
        "look": handle_look,
        "interact": handle_interact,
        "inventory": handle_inventory,
        "trade": handle_trade,
        "help": handle_help,
        "quit": handle_quit
    }

    #---setup room---#
    # initialize room state, everything what is in the room is stored here
    room_state = {"items":[], "interactable_objects":{}, "npcs":{}, "inventory":[]}

    # import the dialog tree from the dragon_room_dialog.py file and create objects starting in the room
    from .dragon_room_dialog import dialogue_tree_cracked_wall, dialogue_tree_blackboard, dialogue_tree_desk, dialogue_tree_chest, dialogue_tree_hole
    room_state["interactable_objects"]["Cracked-Wall"] = {"current_chapter":"first_encounter", "current_node":"start", "dialog_tree":dialogue_tree_cracked_wall}
    room_state["interactable_objects"]["Blackboard"] = {"current_chapter": "first_encounter", "current_node": "start", "dialog_tree": dialogue_tree_blackboard}
    room_state["interactable_objects"]["Desk"] = {"current_chapter": "first_encounter", "current_node": "start", "dialog_tree": dialogue_tree_desk}
    room_state["interactable_objects"]["Chest"] = {"current_chapter": "first_encounter", "current_node": "start","dialog_tree": dialogue_tree_chest}
    room_state["interactable_objects"]["Hole"] = {"current_chapter": "first_encounter", "current_node": "start", "dialog_tree": dialogue_tree_hole}
    room_state["items"].append("Pickaxe")
    #---room setup finished---#

    # start room
    print("You enter the classroom and are immediately drawn to the huge hole in the ground.You see smoke rising from the hole.\n"
          "The chairs and desks of the students are scatterd through the room.\n"
          "Only the teachers desk is still standing on its right place.\n"
          "On the blackboard is something written, but it is to small to read from here.")

    # main loop
    in_room = True
    while in_room:
        command = input("\n> ")
        # transforms input into verb and a noun. Verbs are converted into commands aliases if possible. Cleans articles, prepositions.
        verb, noun = parse(command)

        if verb is None:
            print("What do you want to do?")
            continue

        # Tries to look up my python function(handler) associated with the input string
        handler = commands.get(verb)
        if handler:
            # Calls handler, if it is a function. All handlers return True, unless the room should be exited
            in_room = handler(noun, room_state)
        else:
            print(f"I don't know how to '{verb}'.")

        if "Trophy" in room_state["inventory"]:
            print("You have successfully dealt with the dragon. You can now move on to another room.")
            state["visited"]["dragonroom"] = True
            in_room = False

    # return to the corridor
    return "corridor"
#---end of main function---#