#-----------NPCs-----------#
dialogue_tree_dragon = {
    "first_encounter": {
        "start": {
            "text": "Dragon:'You come to may lair. What do you want?'",
            "options": {
                "1": {"text": "Attempt to attack the dragon",
                      "next_success": "kill_dragon",
                      "next_failure": "failed_attack",
                      "base_success_rate": 0.01,
                      "success_modifiers":{"Broadsword":0.8}},
                "2": {"text": "Try to bribe the Dragon with a Gemstone.",
                      "next_success": "give_gem",
                      "next_failure": "failed_gem",
                      "base_success_rate": 0,
                      "success_modifiers":{"Gemstone":0.5}},
            }
        },
        "kill_dragon": {
            "text": "You slay the beast. Triumphantly you fetch the trophy that it was hiding. You feel heroic and ready to move on to another room.",
            "action":[("give_item","Trophy"), ("remove_npc","Dragon")],
            "next_chapter":"end"
        },
        "failed_attack": {
            "text": "Your attack misses and you are hit by the Dragons claw.",
            "action":("wait",10),
            "next_chapter":"dragon_angry"
        },
        "give_gem": {
            "text": "The Dragon gives you a sceptical look. \nDragon:'Hmm. You really flatter me. I think I am ready to part with this old Trophy' "
                    "\nThe Dragon hands you the Trophy. Satisfied you take the trophy. You feel accomplished and ready to move on to another room.",
            "action":[("give_item","Trophy"), ("remove_npc","Dragon")],
            "next_chapter":"end"
        },
        "failed_gem": {
            "text": "Dragon:'I can see that this Gemstone is fake. Begone.'",
            "next_chapter":"dragon_angry"
        },
    },
    "dragon_angry": {
        "start": {
            "text": "Dragon:'You have made me angry. That is what you get!'\nYou are engulfed in flames.",
            "action":("wait",10),
            "options": {
                "1": {"text": "Attempt to attack the dragon",
                      "next_success": "kill_dragon",
                      "next_failure": "failed_attack",
                      "base_success_rate": 0.01,
                      "success_modifiers":{"Broadsword":0.8}},
            }
        },
        "kill_dragon": {
            "text": "You slay the beast. Triumphantly you fetch the trophy that it was hiding. You feel heroic and ready to move on to another room.",
            "action":[("give_item","Trophy"), ("remove_npc","Dragon")],
            "next_chapter":"end"
        },
        "failed_attack": {
            "text": "Your attack misses and you are hit by the Dragons tail.",
            "action":("wait",10),
            "next_chapter":"dragon_angry"
        },
    }
}

dialogue_tree_fairy = {
    "first_encounter": {
        "start": {
            "text": "Fairy:'Thank you for saving me!'",
            "options": {
                "1": {"text": "Say: 'How will you repay me?'",
                      "next_success": "repay_success",
                      "next_failure": "repay_failure",
                      "base_success_rate": 0.5},
                "2": {"text": "Say: 'Let me know you better. Who are you?'",
                      "next_success": "talk_success",
                      "base_success_rate": 1},
            }
        },
        "repay_success": {
            "text": "Fairy:'You are rude! But I will give you one of my items anyway.'",
            "options": {
                "1": {"text": "Gemstone",
                      "next_success": "gem_success",
                      "next_failure": "repay_failure",
                      "base_success_rate": 0.5},
                "2": {"text": "Broadsword",
                      "next_success": "broadsword_success",
                      "next_failure": "repay_failure",
                      "base_success_rate": 0.2},
            }
        },
        "repay_failure": {
            "text": "The Fairy holds an item out to you. But she snatches it away from you in the last moment and while laughing flies out of the window.",
            "action":("remove_npc","Fairy"),
            "next_chapter":"end"
        },
        "gem_success": {
            "text": "You are a bit perplexed but the Fairy really gives you the item.\nFairy:'Hm, I am done with you. Goodbye!'\nThe Fairy flies out of a window.",
            "action":[("give_item","Gemstone"),("remove_npc","Fairy")],
            "next_chapter":"end"
        },
        "broadsword_success": {
            "text": "You are a bit perplexed but the Fairy really gives you the item.\nFairy:'Hm, I am done with you. Goodbye!'\nThe Fairy flies out of a window.",
            "action":[("give_item","Broadsword"),("remove_npc","Fairy")],
            "next_chapter":"end"
        },

        "talk_success":{
            "text": "Fairy:'I like you. I will help you out if you guess my favorite color.'",
            "options": {
                "1": {"text": "Blue",
                      "next_success": "false_color",
                      "base_success_rate": 1},
                "2": {"text": "Red",
                      "next_success": "false_color",
                      "base_success_rate": 1},
                "3": {"text": "Gold",
                      "next_success": "false_color",
                      "base_success_rate": 1},
                "4": {"text": "Pink",
                      "next_success": "false_color",
                      "base_success_rate": 1},
                "5": {"text": "White",
                      "next_success": "correct_color",
                      "base_success_rate": 1},
                "6": {"text": "Green",
                      "next_success":"false_color",
                      "base_success_rate": 1},
            }
        },
        "false_color": {
            "text": "Fairy:'Maybe I misjudged you. Thank you for your help, but I will leave now.'\nThe Fairy flies out the window.",
            "action":("remove_npc","Fairy"),
            "next_chapter":"end"
        },
        "correct_color": {
            "text": "Fairy:'Bring me as many items of my favorite color and I will reward you!'",
            "next_chapter":"second_encounter"
        },
    },
    "second_encounter": {
        "start": {
            "text": "Fairy:'Have you gathered items of my favorite color for me? What item do you want?'",
            "options": {
                "1": {"text": "Broadsword",
                      "next_success": "give_broadsword",
                      "next_failure": "not_enough_items",
                      "base_success_rate": 0,
                      "success_modifiers": {"Chalk" : 0.33, "Milk-Carton" : 0.33,"Paper" : 0.33,}},
                "2": {"text": "Gemstone",
                      "next_success": "give_gem",
                      "next_failure": "not_enough_items",
                      "base_success_rate": 0,
                      "success_modifiers": {"Chalk" : 0.33, "Milk-Carton" : 0.33,"Paper" : 0.33,}},
            }
        },
        "not_enough_items": {
            "text": "Fairy:'Sorry that's not enough for me. I have wasted my time here. I will leave now.'",
            "action":("remove_npc","Fairy"),
            "next_chapter":"end"
        },
        "give_broadsword": {
            "text": "Fairy:'Here you go. Now you can deal with the dragon!'",
            "action":("give_item","Broadsword"),
            "next_chapter":"last_encounter"
        },
        "give_gem": {
            "text": "Fairy:'Here you go. Now you can deal with the dragon!'",
            "action":("give_item","Gemstone"),
            "next_chapter":"last_encounter"
        },
    },
    "last_encounter": {
        "start": {
            "text": "Fairy:'I have given you all I have. Now go deal with the Dragon.'",
            "next_chapter":"last_encounter"
        }
    }
}

dialogue_tree_kobold = {
    "first_encounter": {
        "start": {
            "text": "The Kobold looks at you with fear.",
            "options": {
                "1": {"text": "Intimidate him",
                      "next_success": "intimidate_success",
                      "next_failure": "intimidate_failure",
                      "base_success_rate": 0.5,
                      "success_modifiers": {"Pickaxe" : 0.1, "Broadsword":0.5}},
                "2": {"text": "Say: 'I will not hurt you.'",
                      "next_success": "talk",
                      "base_success_rate": 1},
            }
        },
        "intimidate_success": {
            "text": "As a offer of peace he drops a Milk-Carton. And flees.",
            "action":("add_item","Milk-Carton"),
            "next_chapter":"fleeing"
        },
        "intimidate_failure": {
            "text": "You looks at you and backs of. But he doesn't look scared of you.",
            "next_chapter":"fleeing"
        },
        "talk": {
            "text": "The Kobold looks surprised that you want to talk to him. But he is still unsure about you.",
            "next_chapter":"talk2"
        },
    },
    "fleeing": {
        "start": {
            "text": "You try to talk to the kobold, but he runs away from you.",
            "next_chapter":"fleeing"
        },
    },
    "talk2":{
        "start": {
            "text": "The Kobold is still unsure about you. But he gets used to your voice.",
            "next_chapter":"talk3"
        },
    },
    "talk3":{
        "start": {
            "text": "The Kobold trust you now. From his hiding spot he fetches a Invisibility-Cloak and hands it to you.",
            "action":("give_item","Invisibility-Cloak"),
            "next_chapter":"follow",
        },
    },
    "follow":{
        "start": {
            "text": "The Kobold follows you around the room. You are not quite sure what to do about that.",
            "next_chapter":"follow"
        },
    }
}
#-----------end NPCs-----------#

#-----interactable object------#
dialogue_tree_cracked_wall = {
    "first_encounter": {
        "start": {
            "text": "There is a crack in the wall. You hear the sound of a someone digging beyond it. Trying to break it open without the right tools could have devastating results.",
            "options": {
                "1": {"text": "Break the wall open.",
                      "next_success": "open_wall",
                      "next_failure": "failed_open_wall",
                      "base_success_rate": 0.4,
                      "success_modifiers": {"Pickaxe" : 0.55}},
            }
        },
        "open_wall": {
            "text": "You break open the wall. A surprised dwarf with a huge backpack looks at you and comes crawling out of the hole. \nShopkeeper: 'Hi I have useful items to trade, if you want.'",
            "action": ("add_npc","Shopkeeper"),
            "next_chapter":"second_encounter"
        },
        "failed_open_wall": {
            "text": "Trying to open the wall lets the other side collapse. Now heavy rubble is blocking the way and there is no way to get through. However you see a Lockpick between the stones.",
            "action":("add_item","Lockpick"),
            "next_chapter":"last_encounter"
        },
    },
    "second_encounter": {
        "start": {
            "text": "The cracked wall has an opening the size of a dwarf.",
            "options": {
                "1": {"text": "Crawl through the opening",
                      "next_success": "crawl_success",
                      "next_failure": "crawl_failure",
                      "base_success_rate": 0.4},
                "2": {"text": "Reach into the hole with you hand.",
                      "next_success": "reach_success",
                      "next_failure": "reach_failure",
                      "base_success_rate": 0.6},
            }
        },
        "crawl_success": {
            "text": "You find a hidden stash of items. What do you want to take?",
                "options": {
                "1": {"text": "Sneaking-Boots",
                      "next_success": "get_sneaking_boots",
                      "base_success_rate": 1},
                "2": {"text": "Lockpick",
                      "next_success": "get_lockpick",
                      "base_success_rate": 1},
            }
        },
        "get_sneaking_boots": {
            "text": "You take the Sneaking-Boots.",
            "action":("give_item","Sneaking-Boots"),
            "next_chapter": "last_encounter"
        },
        "get_lockpick": {
            "text": "You take the Lockpick.",
            "action":("give_item","Lockpick"),
            "next_chapter": "last_encounter"
        },
        "crawl_failure": {
            "text": "You get stuck in the wall. You are not in the mood to try it again.",
            "action":("wait",5),
            "next_chapter": "last_encounter"
        },
        "reach_success": {
            "text": "You find a Lockpick and add it to your inventory.",
            "action":("give_item","Lockpick"),
            "next_chapter": "last_encounter"
        },
        "reach_failure": {
            "text": "You try to reach into the hole, but something sharp cuts your hand. You hear something falling. If there was something in there, now its gone.",
            "action":("wait",5),
            "next_chapter": "last_encounter"
        }
    },
    "last_encounter": {
        "start": {
            "text": "There is nothing to do here anymore.",
            "action":("remove_object","Cracked-Wall"),
            "next_chapter":"end"
            }
    }
}

dialogue_tree_chest = {
    "first_encounter": {
        "start": {
            "text": "A Chest with a heavy lock.",
            "options": {
                "1": {"text": "Break the chest open.",
                      "next_success": "open_chest",
                      "next_failure": "failed_break_chest",
                      "base_success_rate": 0.6,
                      "success_modifiers": {"Pickaxe" : 0.10}},
                "2": {"text": "Try lock picking.",
                      "next_success": "open_chest",
                      "next_failure": "failed_open_chest",
                      "base_success_rate": 0.05,
                      "success_modifiers": {"Lockpick" : 0.90}},
            }
        },
        "open_chest": {
            "text": "You open the chest and a fairy burst out of it. Not the treasure you expected. \nFairy:'I am free!'",
            "action": [("add_npc","Fairy"), ("remove_object", "Chest")],
            "next_chapter":"end"
        },
        "failed_open_chest": {
            "text": "After a while you slip and have to start all over again. Maybe you need the right tools to open the chest... At leats there was no harm done.",
            "action":("wait",5),
            "next_chapter":"first_encounter"
        },
        "failed_break_chest": {
            "text": "You destroy the chest. What ever was in there, now it is destroyed.",
            "action":("remove_object", "Chest"),
            "next_chapter":"end"
        }
    }
}

dialogue_tree_desk = {
    "first_encounter": {
        "start": {
            "text": "The teachers desk has a locked drawer. You get closer to inspect it. However you are startled by a sleeping kobold that lies under the desk.",
            "action":("add_npc", "Kobold"),
            "next_chapter":"second_encounter"
        }
    },
    "second_encounter": {
        "start": {
            "text": "The teachers desk has a locked drawer.",
            "options": {
                "1": {"text": "Break the drawer open.",
                      "next_success": "open_drawer",
                      "next_failure": "failed_break_drawer",
                      "base_success_rate": 0.2,
                      "success_modifiers": {"Pickaxe" : 0.60}},
                "2": {"text": "Try lock picking.",
                      "next_success": "open_drawer",
                      "next_failure": "failed_open_drawer",
                      "base_success_rate": 0.05,
                      "success_modifiers": {"Lockpick" : 0.60}},
            }
        },
        "open_drawer": {
            "text": "You open the drawer. But the only thing inside is a stack of paper that you add to your inventory.",
            "action": [("remove_object", "Desk") , ("give_item","Paper")],
            "next_chapter":"end"
        },
        "failed_open_drawer": {
            "text": "After a while you slip and have to start all over again. Maybe you need the right tools to open the drawer... At leats there was no harm done.",
            "action":("wait",5),
            "next_chapter":"second_encounter"
        },
        "failed_break_drawer": {
            "text": "After you are done with the desk only a pile of wood is left over. Some paper is scatterd through the room.",
            "action":[("remove_object", "Desk") , ("add_item","Paper")],
            "next_chapter":"end"
        },
    }
}

dialogue_tree_hole = {
    "first_encounter": {
        "start": {
            "text": "In the hole you see a huge dragon resting on a pile of gold. You see a Trophy shimmering between the treasurers. \nYou know you want it, but it will be not easy to convince the dragon. \n"
                    "You can also climb into the hole, but with the dragon in there it could be dangerous.",
            "action":("add_npc", "Dragon"), "next_chapter":"second_encounter"
        }
    },
    "second_encounter": {
        "start": {
            "text": "You approach the hole. It will be hard to avoid the dragon.",
            "options": {
                "1": {"text": "Climb into the hole.",
                      "next_success": "climbing_down",
                      "next_failure": "failed_climb",
                      "base_success_rate": 0.3,
                      "success_modifiers": {"Sneaking-Boots" : 0.30, "Invisibility-Cloak":0.40}},
            }
        },
        "climbing_down": {
            "text": "You made it past the Dragon. But to get the Trophy out under him will be even more difficult.",
            "options": {
                "1": {"text": "Try to steal the Trophy.",
                      "next_success": "steal_success",
                      "next_failure": "steal_failure",
                      "base_success_rate": 0.05,
                      "success_modifiers": {"Sneaking-Boots" : 0.30, "Invisibility-Cloak":0.40}},
            }
        },
        "steal_success": {
            "text": "Triumphantly you steal the trophy that the Dragon was hiding. You feel sneaky and ready to move on to another room.",
            "action":[("give_item","Trophy"), ("remove_npc","Dragon")],
            "next_chapter":"end"
        },
        "steal_failure": {
            "text": "You try to steal the Trophy, but the Dragon sees you. \nDragon:'You will not get my treasure!' \nHe flings you out of the hole and moves the Trophy further under his belly.",
            "action":[("wait",10),("make_dragon_angry",None)],
            "next_chapter":"empty"
        },
        "failed_climb": {
            "text": "The Dragon sees you immediately and spits fire at you. \nDragon:'You really tried to steal my treasure?'\nYou retreat immediately.",
            "action":[("wait",10),("make_dragon_angry",None)],
            "next_chapter":"second_encounter"
        },
    },
    "empty": {
        "start": {
        "text": "You approach the hole. It will be hard to avoid the dragon.",
        "options": {
            "1": {"text": "Climb into the hole.", "next_success": "climbing_down", "next_failure": "failed_climb",
                  "base_success_rate": 0.3,
                  "success_modifiers": {"Sneaking-Boots": 0.30, "Invisibility-Cloak": 0.40}}}
        },
        "climbing_down": {
            "text": "You made it past the Dragon. But the trophy is not accessible anymore. Your only option is to leave the hole empty handed.",
            "next_chapter":"empty"
        },
        "failed_climb": {
            "text": "The Dragon sees you immediately and spits fire at you. \nDragon:'You really tried to steal my treasure?'\nYou retreat immediately.",
            "action": ("wait", 10) ,
            "next_chapter": "empty"
        }
    }
}

dialogue_tree_blackboard = {
    "first_encounter": {
        "start": {
            "text": "You see something written on the blackboard, but it is hard to decipher.",
            "options": {
                "1": {"text": "Try to decipher the text. This could really take a long time.",
                      "next_success": "decipher_success",
                      "next_failure": "decipher_failure",
                      "base_success_rate": 0.7},
            }
        },
        "decipher_success": {
            "text": "Written in small letters you read: 'Fairies like to color white.'",
            "action":("wait",10),
            "next_chapter":"second_encounter"
        },
        "decipher_failure": {
            "text": "You can not figure out what is written on the blackboard. By accident you smudge the writing. No it is definitely impossible to decipher the writing...",
            "action":("wait",5),
            "next_chapter":"second_encounter"
        },
    },
    "second_encounter": {
        "start": {
            "text": "There is nothing left to do here. However, you find a small piece of white chalk that you add to your inventory.",
            "action":[("remove_object", "Blackboard"), ("give_item", "Chalk")],
            "next_chapter": "end"
        }
    }
}
#-----interactable object end------#