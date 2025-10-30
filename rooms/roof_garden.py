# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================
import requests
from game.utils import *
from game.db_utils import *

def get_open_meteo_data(parameters):
    # get weather data from open meto api
    url = "https://api.open-meteo.com/v1/forecast"

    response = requests.get(url, params=parameters, timeout=10)
    response.raise_for_status()
    data = response.json()
    if data:
        return data
    else:
        return None

def get_weather():
    #provide parameters for api call
    parameters = {
	"latitude": 52.00362, # Location of THUAS Delft
	"longitude": 4.36668,
	"current": ["rain", "cloud_cover", "temperature_2m","wind_speed_10m","is_day","weather_code"], #specify weather data to get
    }
    try:
        data = get_open_meteo_data(parameters)

        current_temperature_2m = data["current"]["temperature_2m"]  # C
        current_rain = data["current"]["rain"] # mm
        current_cloud_cover = data["current"]["cloud_cover"] # %
        current_is_day = data["current"]["is_day"] #1 day or 0 night
        current_wind_speed = data["current"]["wind_speed_10m"] #km/h
        current_weather_code = data["current"]["weather_code"] # WMO code
    except:
        # If there is a problem with getting the data from the api provide fallback data
        current_temperature_2m = 18
        current_rain = 0
        current_cloud_cover = 0
        current_is_day = 1
        current_wind_speed = 0
        current_weather_code = 0

    # Convert data into levels
    temperature_levels = [(5, 1), (15, 2), (25, 3), (float('inf'), 4)] # eg. 1 level up to 5C, 2 level up to 15C etc
    rain_levels = [(0.5, 1), (2.5, 2), (7.5, 3), (float('inf'), 4)]
    cloud_levels = [(20, 1), (50, 2), (80, 3), (float('inf'), 4)]
    wind_levels = [(5, 1), (20, 2), (40, 3), (float('inf'), 4)]
    temperature_level = get_level(current_temperature_2m, temperature_levels)
    rain_level = get_level(current_rain, rain_levels)
    cloud_level = get_level(current_cloud_cover, cloud_levels)
    day_night = bool(current_is_day)
    wind_level = get_level(current_wind_speed, wind_levels)
    weather_code = get_weather_code_level(current_weather_code)

    return temperature_level, rain_level, cloud_level, day_night, wind_level, weather_code

def get_level(value, levels):
    #helper function to get level of weather phenomenon
    for threshold, level in levels:
        if value < threshold:
            return level

def get_weather_code_level(weather_code):
    #The weather code is just a number. Convert it to a string according to the documentation of open meteo
    weather_phenomenon = None
    if weather_code in [45, 48]:
        weather_phenomenon = "fog"
    elif weather_code in [71, 73, 75, 77, 85, 86]:
        weather_phenomenon = "snow"
    elif weather_code in [95, 96, 99]:
        weather_phenomenon = "thunderstorm"
    return weather_phenomenon

def add_bonus_to_dice(state, bonus):
    # Add a number to all dice and make sure the new number is between 1 and 6
    dice = state["roof_garden"]["dice"]
    for i in range(len(dice)):
        dice[i] = max(1, min(dice[i]+bonus, 6))

def convert_dice_to_faces(dice):
    # Convert number to dice face
    dice_faces = [None, "⚀","⚁", "⚂", "⚃", "⚄", "⚅"]
    return [dice_faces[item] for item in dice]

#---action functions---#
def water_orchid(state):
    print("You water the orchid. It seams in much better state already.")
    state["roof_garden"]["orchid"]["water"] = True

def add_fertilizer(state):
    print("You add fertilizer to the orchid. The earth is now much better suited for it.")
    state["roof_garden"]["orchid"]["fertilizer"] = True

def eat_berry(state):
    print("The berry has a sweet taste.")
    add_bonus_to_dice(state, -2)

def repair_robot(state):
    print("The gardening robot springs to life. It takes up a pair of clippers and starts to carefully tend to the orchid.")
    print("The orchid looks much better now.")
    state["roof_garden"]["orchid"]["robot"] = True
    if len(state["roof_garden"]["dice"]) == 2: # if there are exactly two dice left combine them
        dice1 = state["roof_garden"]["dice"][0]
        dice2 = state["roof_garden"]["dice"][1]
        new_dice = min(dice1 + dice2, 6)
        state["roof_garden"]["dice"] = [new_dice]
    elif len(state["roof_garden"]["dice"]) > 2: # if more than two dice, let the player decide
        print(f"\nEnter two dice to be combined together from you dice {' '.join(convert_dice_to_faces(state['roof_garden']['dice']))}:")
        while True:
            dice1 = input("Choose the first die: ") # input first die and check if in player dice
            try:
                dice1 = int(dice1)
            except ValueError:
                print("Please enter a number.")
            if dice1 in state["roof_garden"]["dice"]:
                state["roof_garden"]["dice"].remove(dice1) # remove first die
                break
            else:
                print("Enter one of your dice.")
        while True:
            dice2 = input("Choose the second die: ")  # input second die and check if in player dice
            try:
                dice2 = int(dice2)
            except ValueError:
                print("Please enter a number.")
            if dice2 in state["roof_garden"]["dice"]:
                state["roof_garden"]["dice"].remove(dice2)  # remove second die
                break
            else:
                print("Enter one of your dice.")
        new_dice = min(dice1 + dice2, 6) #combine dice together and make sure it is less or equal to 6
        state["roof_garden"]["dice"].append(new_dice) #add new die to dice
    else: # if 1 or 0 dice left don't combine anything
        print("You don't have enough dice to combine.")

def search_garden(state):
    print("You see a hammock spanned between two berry bushes. A garden robot is standing still, as if it is rusted in place.")
    print("A black shadow startles you. However it is just a cat.")
    state["roof_garden"]["actions"]["lay_hammock"] = {"text": "Lay in hammock", "description": "+1 to all dice", "dice": [1, 2, 3, 4, 5, 6], "action": lay_hammock}
    state["roof_garden"]["actions"]["pet_cat"] = {"text": "Pet cat", "dice": [5, 6], "action": pet_cat}
    state["roof_garden"]["actions"]["repair_robot"] = {"text": "Repair garden robot", "description": "combine two dice together", "dice": [5, 6], "action": repair_robot}
    state["roof_garden"]["actions"]["eat_berry"] = {"text": "Eat berry", "description": "-2 to all dice", "dice": [3, 4, 5, 6], "action": eat_berry}

def pet_cat(state):
    print("MEOW! At first the cat is scared of you. However you approach it very carefully and pet it. The purring of the cat calms you.")
    db_award_achievement(state, "pet_cat")

def lay_hammock(state):
    print("You take a relaxing nap in the hammock. You feel much more relaxed.")
    add_bonus_to_dice(state, 1)
#---end action functions---#

#---handler functions---#
def handle_talk_gardener(state):
    if db_get_room_completed(state, "roof_garden"):
        print("Gardener: You inspired me. I will make the whole garden bloom again.")
        return
    if not state["roof_garden"]["dice"]:
        print("Gardener: You exhausted all your energy. Come back later to start again.")
    weather = state["roof_garden"]["weather"]
    if weather == "rain":
        print("The gardener is holding an umbrella, water dripping from her coat.")
    elif weather == "wind":
        print("The gardener is cowering under a blanket to shield herself from the wind.")
    elif weather == "mild":
        print("The gardener is sitting in a garden chair with a cup of tea. She looks at you and sneezes.")
    print("Gardener: I am sick today, can you tend to my priced orchid? Without attention it will wither away.")
    print(f"Gardener: Make sure to {Color.green}water{Color.end} it, find some {Color.green}fertilizer{Color.end} and activate the {Color.green}garden robot{Color.end}.")
    print("Gardener: Gardening can be exhausting. So keep in mind that you have limited amount of things you can do in this room, before getting exhausted.")
    print("Your energy is represented by dice. You have to choose one die for each action and it must be a correct die, specified by each action.")
    print("If you have spend your dice on the wrong things, leave the room and come back later to start again.")

def handle_look_greenhouse(state):
    if db_get_room_completed(state, "roof_garden"):
        print("The orchid in the greenhouse is blooming magnificently.")
    else:
        print("In the greenhouse you see a orchid. However, looks a bit neglected.")

def handle_help(state):
    print("Roof Garden commands:")
    print("- talk gardener       : Talk to the gardener.")
    if state["roof_garden"]["talked_to_gardener"] and state["roof_garden"]["dice"]:
        for key, value in state["roof_garden"]["actions"].items():
            print(f"- {value['text']} <dice-number>")
#---end handler functions---#

def roof_garden_enter(state):
    if db_get_room_completed(state, "roof_garden"): # If already completed dont let player enter
        print("You have already successfully tended to the garden.")
        return False

    state["roof_garden"] = {"weather": None, "actions": None, "talked_to_gardener": False, "dice": [], "orchid": {"water": False, "fertilizer": False, "robot": False}}

    temperature, rain, cloud_cover, is_day, wind_speed, weather_code = get_weather() # get current weather
    temperature_adjective = {1:"freezing", 2:"cold", 3:"mild",  4:"hot"}
    # Print intro messages of the current weather:
    print(f"You enter a classroom, but are surprised that you are feeling the {temperature_adjective[temperature]} air from outside.")
    print("The ceiling windows are open letting the elements in.")
    if is_day:
        if cloud_cover < 3:
            print("The sun is shining through the open ceiling windows.")
        else:
            print("You see the sky, through the open ceiling windows, but the sun is hidden behind clouds.")
    else: # at night
        print("The sun has already set but the room is illuminated by multiple lamps.")
        if cloud_cover < 3:
            print("You see the moon through the open ceiling windows.")
        else:
            print("The sky is pitch black. There is no sign of stars or the moon behind the clouds.")
    if weather_code == "snow":
        print("Small white flocks of snow are slowly drifting through the windows.")
        print("Snow is piling up on the floor.")
    elif rain == 2:
        print("A light drizzle is coming trough the windows filling the room with moisture.")
    elif rain >= 3:
        print("Rain is pouring through the open windows.")
    if rain > 1:
        print("Puddles are forming on the floor.")

    if wind_speed == 2:
        print("You feel a soft breeze.")
    elif wind_speed == 3:
        print("The wind is rattling on the windows.")
    elif wind_speed == 4:
        print("It is hard to stay upright, the wind is pushing and pulling on you.")

    if weather_code == "thunderstorm":
        print("You are startled by a flash of a lightning and the loud roar of thunder.")
    elif weather_code == "fog":
        print("You can barely make out your hands in front of you due to thick fog in the room.")

    # Set current scenario dice from mild weather, rain, or wind
    if rain < 2 and wind_speed < 3:
        weather = "mild"
        dice = [1,2,3,3,3,4]
    elif rain > wind_speed:
        weather = "rain"
        dice = [3,3,4,4,5,6]
    else:
        weather = "wind"
        dice = [1,1,2,2,2,6]

    state["roof_garden"]["weather"] = weather
    state["roof_garden"]["dice"] = dice

    print("\nThe classroom is filled with plants, it is like a jungle in here. You push some leaves to the side to get to the center of the room.")
    print("You see a gardener beside a small greenhouse with a plant inside it.")
    # Available actions at the beginning
    actions = {
        "search_garden": {"text": "Search garden", "dice": [1 ,2 ,3 , 4, 5, 6], "action":search_garden},
        "add_fertilizer": {"text": "Add fertilizer", "dice": [6], "action": add_fertilizer},
        "water_orchid ": {"text": "Water orchid", "dice": [1], "action": water_orchid},
    }
    state["roof_garden"]["actions"] = actions
    return True

def roof_garden_commands(command, state):
    command_executed = False
    if command == "talk gardener":
        handle_talk_gardener(state)
        state["roof_garden"]["talked_to_gardener"] = True
        command_executed = True
    elif command == "help" or command == "?":
        handle_help(state)
        command_executed = True
    elif command == "look around":
        print("You are in the middel of a garden. You see a gardener beside a greenhouse with a plant inside.")
        command_executed = True
    elif command == "look greenhouse" or command == "look orchid" or command == "look plant":
        handle_look_greenhouse(state)
        command_executed = True

    if state["roof_garden"]["talked_to_gardener"]: # check action commands and  print action dice if you talked to gardener
        for key, item in state["roof_garden"]["actions"].items():
            if item["text"].lower() == command[:-2]: # If action with dice was entered execute it
                command_executed = True
                try:
                    input_dice = int(command[-1])
                except ValueError:
                    print("Make sure to type in a number representing one of your dice after each command.")
                    break
                if not input_dice in state["roof_garden"]["dice"]:
                    print("You don't have a die with that value. Please select a dice from your energy dice.")
                    break
                if input_dice in item["dice"]:
                    state["roof_garden"]["dice"].remove(input_dice) # remove spend dice
                    item["action"](state) # call function associated with the chosen action
                    if not command[:-2] == "lay in hammock": # Delete the action, you can only do it once. Except if it is 'lay in hammock', this can be performed multiple times
                        del state["roof_garden"]["actions"][key]
                    break
            elif item["text"].lower() == command: # If the player just entered the action, but not a die remind them to enter a die
                command_executed = True
                print("Make sure to type in a number representing one of your dice after each command.")
        print("")
        if state["roof_garden"]["dice"]: # If there are dice left, print dice and all available action with their associated dice
            print(f"Your energy dice: {' '.join(convert_dice_to_faces(state['roof_garden']['dice']))}")
            for key, value in state["roof_garden"]["actions"].items():
                print(f"\n{value['text']} {'/'.join(convert_dice_to_faces(value['dice']))}", end='')
                if value.get('description', False):
                    print(f": This will result in {value.get('description')}", end='')
        print("")

    if state["roof_garden"]["orchid"]["water"] and state["roof_garden"]["orchid"]["fertilizer"] and state["roof_garden"]["orchid"]["robot"]:
        # If the player fulfilled all necessary tasks, print the end message and complete roof garden
        print("The orchid starts to bloom.")
        print("Gardener: Thank you for helping me out!")
        db_mark_room_completed(state, "roof_garden")
        print("Gardener: I don't have much to give, but I have this beautiful rose I can give you.")
        print("The gardener doesn't seam to notice the dark aura coming from the rose. You still take it and put it in your inventory.")
        db_add_item_to_inventory(state, "cursed_rose")

    if not state["roof_garden"]["dice"]: #Remind the player to come back later if they have no more dice, or if they finished that they should move on
        if db_get_room_completed(state, "roof_garden"):
            print("You spent all your energy. With the task completed you are ready to move on to another room.")
        else:
            print("You spent all your energy. You have to come back later to start over.")

    return command_executed