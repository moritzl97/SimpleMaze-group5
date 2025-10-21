# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================

# This file contains all functions of the dragon room.
# Scroll down to the main function enterDragon Room() which is called when the dragon room is entered.

import random
import time
from game.utils import *
from game.db_utils import *
from rooms.dragon_room_db_utils import *

#---define open dialog---#
# Called if player talks to an NPC or interacts with objects
def open_dialog(name, state):
    # Loop through all dialog nodes in the current chapter. Ends if the chapter is finished
    dialog = db_get_dialog(state, name)
    while True:
        #get current dialog node by looking up the current chapter and node for the npc
        (chapter_index, node_index) = db_get_chapter_node_index(state, name)
        node = dialog[chapter_index][node_index]

        # Print dialog text
        print(f"{node['text']}")

        # Call function if there is an action defined at this point in the dialog
        if "action" in node:
            #lookup the function that should be called from the dialog
            actions = node["action"]
            if type(actions[0]) != list:
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
            db_save_chapter_node(state, name, "start", node["next_chapter"])
            return

        # If there are options print all of them
        print("\nChoices:")
        for option_number, option_entry in node["options"].items():
            # Calculate success rate and see if helpful items are in the players inventory
            success_rate = option_entry["base_success_rate"]
            added_modifier_list = []
            for item, modifier in option_entry.get("success_modifiers", {}).items():
                if db_is_item_in_inventory(state, item):
                    success_rate += modifier
                    added_modifier_list.append(item)

            # Cap success rate if to many bonuses were added
            if success_rate > 1:
                success_rate = 1

            # Print option number, the text and the success rate if you choose this option
            print(f" {option_number}. {option_entry['text']} ({int(success_rate*100)}%) ")
            # If there are items that helped, list them
            if added_modifier_list:
                print(f"    Helping items: {', '.join(added_modifier_list)}")

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
                    if db_is_item_in_inventory(state, item):
                        success_rate += modifier
                if success_rate > 1:
                    success_rate = 1
                # Roll the dice and see if successful or failure:
                if success_rate > random.uniform(0, 1):
                    db_save_chapter_node(state, name, option_entry["next_success"]) # set the next dialog to success
                    print(f"{Color.green}Success!{Color.end}")
                else:
                    db_save_chapter_node(state, name, option_entry["next_failure"])# set the next dialog to failure
                    print(f"{Color.red}Failure!{Color.end}")
                break # go back to the first loop and print the next dialog node
#---end talk definition---#

#---define shop keeper---#
def trade_with_shopkeeper(npc, state):
    #Get items that the shopkeeper wants to trade
    trades = db_get_trades(state)

    if not trades:
        print("I have nothing to trade anymore.")
        return

    print("I will trade the following items with you:")
    while True:
        number_of_options = len(trades)+1
        for index in range(1, number_of_options):
            print(f"{index}. Sell a {trades[index-1][2]} for a {trades[index-1][1]}")
        print(f"{number_of_options}. I don't want to trade.")

        choice = int(input("\n> ").strip())

        if choice < number_of_options:
            trade_id = trades[choice-1][0]
            item_sell = trades[choice-1][1]
            item_wanted = trades[choice-1][2]
            # Check if the player really has the item that he want to give the shopkeeper in the inventory
            if db_is_item_in_inventory(state, item_wanted):
                db_remove_item_from_inventory(state, item_wanted)
                db_add_item_to_inventory(state, item_sell)
                db_remove_trade(state, trade_id)
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
    db_add_object_to_room(state, argument, "npcs")

def add_item(argument, state):
    #Adds item to the room
    db_add_object_to_room(state, argument, "items")

def give_item(argument, state):
    #Adds item to players inventory
    db_add_item_to_inventory(state, argument)

def remove_object(argument, state):
    # Remove object from room
    db_remove_object_from_room(state, argument, "objects")

def remove_npc(argument, state):
    #Remove npc from room
    db_remove_object_from_room(state, argument, "npcs")

def try_remove_item_from_inv(argument, state):
    # Remove item from inventory, if it is in the inventory
    db_remove_item_from_inventory(state, argument)

def make_dragon_angry(argument, state):
    # Sets the next dialog of the dragon to angry
    db_save_chapter_node(state, "dragon", "start", "dragon_angry")

#---End of action functions---#

#---Command handlers---#
def handle_look(noun, state):
    if noun:
        # States where the given noun is (if in the room)
        if db_check_if_in_room(state, noun, "items"):
            print(f"You look at the {noun}. It might be useful if you pick it up.")
        elif db_check_if_in_room(state, noun, "npcs"):
            print(f"You look at the {noun}. You can talk to them if you want to.")
        elif db_check_if_in_room(state, noun, "objects"):
            open_dialog(noun, state)
        elif db_is_item_in_inventory(state, noun):
            print(f"You find {noun} in your inventory.")
        else:
            print(f"You don't see a {noun} here.")
    else:
        #Prints a description of the room and lists all things that are in the room
        print("You are in a classroom with a huge hole in the ground. You see smoke rising from the hole.\n"
              "The chairs and desks of the students are scatterd throughout the room.\n"
              "Only the teacher's desk is still standing on its right place.\n"
              "On the blackboard is something written, but it is to small to read from here.\n")
        items = db_get_objects_in_room(state, "items")
        if items:
            print(f"You see the following items in the room: {', '.join(items)}")
        npcs = db_get_objects_in_room(state, "npcs")
        if npcs:
            print(f"You can talk to the following NPCs in the room: {', '.join(npcs)}")
        objects = db_get_objects_in_room(state, "objects")
        if objects:
            print(f"You see these points of interest in the room: {', '.join(objects)}")
    return

def handle_take(noun, state):
    #Pick up item and add it to inventory
    if not noun:
        print("Take what?")
    elif db_is_item_in_inventory(state, noun):
        print(f"You already have the {noun} in your inventory.")
    elif db_check_if_in_room(state, noun, "items"):
        db_remove_object_from_room(state, noun, "items")
        db_add_item_to_inventory(state, noun)
        print(f"You take {noun}.")
    else:
        print(f"You cannot pickup {noun}.")
    return

def handle_trade(noun, state):
    # opens trade menu with the shopkeeper
    if db_check_if_in_room(state, "shopkeeper", "npcs"):
        trade_with_shopkeeper("shopkeeper", state)
    else:
        print("There is nobody to trade with here.")
    return

def handle_interact(noun, state):
    # opens dialog with an object or a npc
    if not noun:
        print("Interact with what?")
    else:
        if db_check_if_in_room(state, noun, "objects"):
            open_dialog(noun, state)
        elif db_check_if_in_room(state, noun, "npcs"):
            if noun == "shopkeeper":
                trade_with_shopkeeper("shopkeeper", state)
            else:
                #Print ASCII art if you talk with dragon
                if noun == "dragon":
                    print(Color.red+r"""                                              /(  /(
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
                                                                                       /.-~"""+Color.end)

                open_dialog(noun, state)
        else:
            print(f"There is no {noun} here to interact with.")
    return

def handle_help(noun, state):
    # list commands
    print("Dragon Room commands:")
    print("Type in a verb and a noun to interact with the things in the room.\nType 'look around' to see what is in the room. \nUse verbs lik: 'look', 'talk', 'inspect', 'trade' and 'take'")

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
        noun = "_".join(words[1:])

    return verb, noun
# ---Parser end---#

#---Main functions---#
# Called when dragon room is entered
def dragon_room_enter(state):
    # If player has finished the dragon room print this message and return them to the corridor
    if state["completed"]["dragon_room"]: #TODO change completed to db
        print("You have already dealt with the dragon and are ready to move on to another room.")
        return False

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

    if db_is_item_in_inventory(state, "Trophy"):
        print("You have successfully dealt with the dragon. You can now move on to another room.")
        state["completed"]["dragon_room"] = True # TODO change completed to db

    return False
