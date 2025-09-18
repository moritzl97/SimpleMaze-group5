import random
import time

#---define talk---#
# Called if player talks to an NPC or interacts with objects
def interact(npc, room_state):
    # if dialog branch is exhausted display this:
    if npc["current_chapter"] not in npc["dialog_tree"]:
        print(f"{npc["name"]} has nothing more to say.")
        return

    # Define which string calls which function
    action_map = {
        "wait": wait,
        "add_npc": add_npc,
        "give_item": give_item,
        "remove_object": remove_object,
        "add_item": add_item
    }

    # Loop through the dialog nodes in the branch
    while True:
        #get current dialog node
        node = npc["dialog_tree"][npc["current_chapter"]][npc["current_node"]]

        # Run node action if defined
        if "action" in node:
            if type(node["action"]) == list:
                for executable_action in node["action"]:
                    function, argument = executable_action
                    function = action_map.get(function)
                    if callable(function):
                        function(argument, room_state)
                    else:
                        raise Exception(f"Action function {node["action"]} missing")
            else:
                function, argument = node["action"]
                function = action_map.get(function)
                if callable(function):
                    function(argument, room_state)
                else:
                    raise Exception(f"Action function {node["action"]} missing")

        # Print node text
        if npc.get("name"):
            print(f"{npc["name"]}: '{node["text"]}'")
        else:
            print(f"{node["text"]}")

        # If there are no branching dialog options end dialog
        if "next_chapter" in node:
            npc["current_chapter"] = node["next_chapter"]
            npc["current_node"] = "start"
            return

        # If there are options print all of them
        print("\nChoices:")
        for option_number, option_entry in node["options"].items():
            # Calculate success rate and see if helpful items are in the players inventory
            added_modifier_list = []
            success_rate = option_entry["base_success_rate"]
            # Look through the possible modifiers that can help for this option
            if "success_modifiers" in option_entry:
                for item, modifier in option_entry["success_modifiers"].items():
                    # If helpful item is in inventory add modifier to success rate and store the item that helped
                    if item in room_state["inventory"]:
                        success_rate += modifier
                        added_modifier_list.append(item)

            # Cap success rate if to many bonuses were added
            if success_rate > 1:
                success_rate = 1

            # Print option number, the text and the success rate if you choose this option
            print(f" {option_number}. {option_entry["text"]} ({int(success_rate*100)}%) ")
            # If there are items that helped, list them
            if added_modifier_list:
                print("Helping items: ")
                for item in added_modifier_list:
                    print(f"{item} ")

        print(f" {len(node["options"])+1}. Leave")

        # Input loop
        # Checks if the player entered a valid option
        while True:
            choice = input("\n> ").strip()
            # Check if player selected leave option
            if choice == str(len(node["options"])+1):
                print("You back of to do something else.")
                return
            # If choice is in options check for success, else ask again for an input
            if choice in node["options"]:
                # Calculate success rate (again)
                success_rate = node["options"][choice]["base_success_rate"]
                if "success_modifiers" in node["options"]:
                    for item, modifier in node["options"][choice]["success_modifiers"].items():
                        if item in room_state["inventory"]:
                            success_rate += modifier
                # Cap success rate if to many bonuses were added
                if success_rate > 1:
                    success_rate = 1

                # Make the dice roll to determine success or failure
                if success_rate > random.uniform(0, 1):
                    #Print success and go to success dialog
                    npc["current_node"] = node["options"][choice]["next_success"]
                    print("Success!")
                else:
                    # Print failure and go to failure dialog
                    npc["current_node"] = node["options"][choice]["next_failure"]
                    print("Failure!")
                # go back to the first loop and go to the next dialog node
                break
            else:
                print("Please choose a valid option.")
#---end talk definition---#

#---define shop keeper---#
def trade_with_shopkeeper(npc, room_state):

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
    words = user_input.lower().split()

    fluff = {"the", "a", "an", "to", "up", "with", "around"}
    words = [word for word in words if word not in fluff]

    if not words:
        return None, None

    verb = words[0]
    noun = None

    verb_aliases = {
        "inspect": "look",
        "examine": "look",
        "check inventory": "inventory",
        "inv": "inventory",
        "pick": "take",
        "grab": "take",
        "walk": "go",
        "move": "go",
        "use": "interact",
        "sell": "trade",
        "buy": "trade"
    }

    if verb in verb_aliases.keys():
        verb = verb_aliases[verb]

    if len(words) > 1:
        noun = words[1].title()

    return verb, noun
#---Parser end---#

#---Command handlers---#
def handle_look(noun, room_state):
    if noun:
        if noun in room_state["items"]:
            print(f"You look at the {noun}. It might be useful if you pick it up.")
        elif noun in room_state["npcs"]:
            print(f"You look at the {noun}. You can talk to them if you want to.")
        elif noun in room_state["interactable_objects"]:
            interact(room_state["interactable_objects"][noun], room_state)
        elif noun in room_state["inventory"]:
            print(f"You find the {noun} in your inventory.")
        else:
            print(f"You don't see a {noun} here.")
    else:
        print("You are in a classroom with a huge hole in the ground. You see smoke rising from the hole. The chairs and desks of the students are scatterd through the room."
          "Only the teachers desk is still standing on its right place. "
          "On the blackboard is something written, but it is to small to read from here.")
        if room_state['items']:
            print(f"You see the following items in the room: {", ".join(room_state['items'])}")
        if room_state['npcs']:
            print(f"You can talk to the following NPCs in the room: {", ".join(room_state['npcs'].keys())}")
        if room_state['interactable_objects']:
            print(f"You see these points of interest in the room: {", ".join(room_state['interactable_objects'].keys())}")

    return True

def handle_go(noun, room_state):
    if not noun:
        print("Go to which room?")
        return True
    if noun.lower() in ["corridor", "back"]:
        print("You flee the dragon room.")
        return False
    else:
        print(f"You can't go to '{noun}' from here.")
        return True

def handle_take(noun, room_state):
    if not noun:
        print("Take what?")
        return True
    if noun in room_state["inventory"]:
        print(f"You already have the {noun} in your inventory.")
    elif noun in room_state["items"]:
        room_state["items"].remove(noun)
        room_state["inventory"].append(noun)
        print(f"You take the {noun}.")
    else:
        print(f"You cannot pickup {noun}.")
    return True

def handle_trade(noun, room_state):
    for npc in room_state["npcs"]:
        if npc == "Shopkeeper":
            trade_with_shopkeeper(npc, room_state)
            break
        else:
            print("There is nobody to trade with here.")
    return True

def handle_interact(noun, room_state):
    if not noun:
        print("Interact with what?")
    else:
        if noun in room_state["interactable_objects"]:
            interact(room_state["interactable_objects"][noun], room_state)
        else:
            print(f"There is no {noun} here to interact with.")
    return True


def handle_talk(noun, room_state):
    if not noun:
        print("You mutter to yourself...")
        return True

    for npc in room_state["npcs"]:
        if npc == noun:
            if npc == "Shopkeeper":
                trade_with_shopkeeper(npc, room_state)
            else:
                interact(room_state["npcs"][npc], room_state)
            return True

    print(f"There is no {noun} here.")
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
    print("Type in a verb and a noun to interact with the things in the room.")
#---Command handlers finished---#

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
        room_state["npcs"]["Shopkeeper"] = {"name": "Shopkeeper", "items_for_sale": ["Broadsword","Sneaking-Boots","Lockpick"], "wanted_items": ["Gemstone","Chalk","Pickaxe"]}
    elif argument == "Fairy":
        from .dragon_room_dialog import dialogue_tree_fairy
        room_state["npcs"]["Fairy"] = {"name":"Fairy", "current_chapter":"first_encounter", "current_node":"start", "dialog_tree":dialogue_tree_fairy}
    elif argument == "Kobold":
        from .dragon_room_dialog import dialogue_tree_kobold
        room_state["npcs"]["Kobold"] = {"name":"Kobold", "current_chapter":"first_encounter", "current_node":"start", "dialog_tree":dialogue_tree_kobold}
    elif argument == "Dragon":
        from .dragon_room_dialog import dialogue_tree_dragon
        room_state["npcs"]["Dragon"] = {"name": "Dragon", "current_chapter": "first_encounter", "current_node": "start", "dialog_tree": dialogue_tree_dragon}

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

def make_dragon_angry(argument, room_state):
    room_state["npcs"]["Dragon"]["current_chapter"] = "dragon_angry"
    room_state["npcs"]["Dragon"]["current_node"] = "start"
#---End of action functions---#

#---Main function---#
# Called when dragon room is entered
def enterDragonRoom(state):

    if state["visited"]["dragonroom"] == True:
        print("You have already dealt with the dragon and are ready to move to another room.")
        return "corridor"

    # dict to store command handler functions
    commands = {
        "go": handle_go,
        "take": handle_take,
        "look": handle_look,
        "interact": handle_interact,
        "talk": handle_talk,
        "inventory": handle_inventory,
        "trade": handle_trade,
        "help": handle_help
    }

    #---setup room---#
    # initialize room state
    room_state = {"items":[], "interactable_objects":{}, "npcs":{}, "inventory":[]}

    # dialog dicts
    # store all data related to the branching dialog for one NPC
    # stores: different encounters-> dialog nodes-> (text, action, options->(text, next_success, next_failure, base_success_rate, success_modifiers->(item, modifier)))
    example_dialog = {
        "first_encounter": {
            "start": {
                "text": "Displayed text",
                "action": None, # Function to call if available
                "options": { # Options for the player to choose
                    "1": {"text": "Option text", "next_success": "yes", "next_failure": "no",
                          "base_success_rate": 1, "success_modifiers": {}},
                    "2": {"text": "Give the dragon 100 gold", "next_success": "happy",
                          "next_failure": "angry", "base_success_rate": 0.5, "success_modifiers": {}},
                }
            },
            "yes": {
                "text": "Text if success",
                "action": None,
                "next_chapter": "second_encounter" # next dialog chapter
            },
        },
        "second_encounter": { # next chapter
            "start": {
                "text": "I am done with you.",
                "next_chapter": "end"
            }
        }
    }

    # import the real dialog tree from the dragon_room_dialog.py file
    from .dragon_room_dialog import dialogue_tree_cracked_wall, dialogue_tree_blackboard, dialogue_tree_desk, dialogue_tree_chest, dialogue_tree_hole

    #create objects
    room_state["interactable_objects"]["Cracked-Wall"] = {"current_chapter":"first_encounter", "current_node":"start", "dialog_tree":dialogue_tree_cracked_wall}
    room_state["interactable_objects"]["Blackboard"] = {"current_chapter": "first_encounter", "current_node": "start", "dialog_tree": dialogue_tree_blackboard}
    room_state["interactable_objects"]["Desk"] = {"current_chapter": "first_encounter", "current_node": "start", "dialog_tree": dialogue_tree_desk}
    room_state["interactable_objects"]["Chest"] = {"current_chapter": "first_encounter", "current_node": "start","dialog_tree": dialogue_tree_chest}
    room_state["interactable_objects"]["Hole"] = {"current_chapter": "first_encounter", "current_node": "start", "dialog_tree": dialogue_tree_hole}
    #---room setup finished---#

    # start room
    print("You enter the classroom and are immediately drawn to the huge hole in the ground. You see smoke rising from the hole. The chairs and desks of the students are scatterd through the room."
          "Only the teachers desk is still standing on its right place. "
          "On the blackboard is something written, but it is to small to read from here.")
    in_room = True
    # main loop
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