import random

nu_of_hero = 0
nu_of_stage = 0
heroes = [] #List of heroes
stages = [] #List of stages
hero = {}
boss = {"name": "", "hp": 0}
current_location = 0
potion_remaining = 3

# Main Page
print("")
print("—————————————————————————")
print(" — THE DEATHLY HALLOWS — ")
print("—————————————————————————")
print("")


# prompt user to enter a name
name = input("Please enter your name: ")
print("")
print("Welcome to THE DEATHLY HALLOWS,", name, "!")
print("------------------------------------------------------------------")
    

def get_hero_data():
    hero_file = open("heroes.txt", "r")
    global nu_of_hero
    nu_of_hero = int(hero_file.readline())
    
    for x in range (0, nu_of_hero - 1):
        hero_value = hero_file.readline() #Read 1 line from the text file
        #Split by delimeter
        name, hp, damage, specialskillname, specialskill = hero_value.split(",")
        #Hero dictionary
        hero = {
            "name": name,
            "hp": hp,
            "n": damage, #normal skill damage
            "specialskillname": specialskillname,
            "s": specialskill, #special skill damage
            "h": 500
        }
        heroes.append(hero) #Add the hero to the list
    boss_value = hero_file.readline() #Read the boss line
    boss["name"], boss["hp"] = boss_value.split(",")
    # print(hero)
    hero_file.close()

def get_event_data():
    event_file = open("event.txt", "r")
    global nu_of_stage
    nu_of_stage = int(event_file.readline())
    
    for x in range (0, nu_of_stage):
        hero_value = event_file.readline()
        location, title, damage = hero_value.split("|")
        stage = {
            "location": location,
            "title": title,
            "damage": damage
        }
        stages.append(stage)
    event_file.close()


def show_menu():    
    i = -1
    user_choice = ""         

    while user_choice.lower() != "s":
        user_choice = ""
        if(i == nu_of_hero - 2): i = -1 
        #Reset the list position
        i += 1
        global hero #get the global value of hero
        hero = heroes[i] #save selected hero
        #print hero information
        print("Hero Number ", i + 1)
        print("Name:", hero["name"])
        print("HP:", hero["hp"])
        print("Attack damage:", hero["n"]) #normal damage
        print("Special Skill Name:", hero["specialskillname"])
        print("Special Skill Damage:", hero["s"]) #special skill damage
        while user_choice.lower() != 'n' and user_choice.lower() !='s':
            user_choice = input("Press S to select hero or N to view the next hero:")

    print("You have chose ",hero["name"])
    print("-------------------------------------------")

def show_stage_info(rolled_result, stage, current_hp, old_hp):
    print("-------------------------------------------")
    print("You have rolled ", rolled_result)
    print("Location: ", stage['location'])
    print(stage['title'])
    print("Health point: ", stage['damage'])
    print("Hero health: ", current_hp, " (",old_hp,")")
    print("-------------------------------------------")


def roll_the_dice():
    result = random.randint(1, 6)
    global current_location         # Update
    current_location += result      # current location
    go_to_location(result, current_location)

def go_to_location(rolled_result, location):
    if location >= 10:
        location = 10
        print("You have rolled ", rolled_result)
        print("Welcome to the Hogwarts Courtyard")
        print(stages[location - 1]['title'])
        fight_the_boss()
    #Update hero hp
    global hero                    
    current_hp = int(hero["hp"])   
    hero["hp"] = int(stages[location - 1]['damage']) + current_hp
    #Show stage information
    show_stage_info(rolled_result, stages[location - 1], hero["hp"], current_hp)
    #continue to roll
    input("Press enter to roll the dice")
    roll_the_dice()

def boss_attack():
    damage = random.randint(300, 1000)
    print(boss["name"]," attacks you with ", damage, " damage")
    return damage

def player_attack():
    #get hero skill damage or health
    global hero
    global potion_remaining
    damage = 0
    #show skill options
    if potion_remaining > 0:
        chosen_skill = ""
        print("[N]ormal attack | [S]pecial skill | [H]ealth potion")
        while chosen_skill.lower() != 'n' and chosen_skill.lower() != 's' and chosen_skill.lower() != 'h':
            chosen_skill = input("Your choice: ")
    else:
        chosen_skill = ""
        print("[N]ormal attack | [S]pecial skill")
        while chosen_skill.lower() != 'n' and chosen_skill.lower() != 's':
            chosen_skill = input("Your choice: ")
    print("-------------------------------------------")

    #branching for skill
    if chosen_skill.lower() == 'h': #health potion
        if potion_remaining > 0:
            hero["hp"] = int(hero["hp"]) + 500  #update player hp
            potion_remaining -= 1 #reduce the potion remaining
            print(hero["name"]," hp has increase to", hero["hp"],"(+500)")
    else:
        damage = int(hero[chosen_skill.lower()])
        print(hero["name"]," attacks with ", damage, " damage")
    return damage
    
def fight_the_boss():
    turn = 0
    while True:
        global hero
        global boss
        if turn%2==0:
            #player turn
            #update the boss hp
            boss["hp"] = int(boss["hp"]) - int(player_attack())
            show_turn_info(boss["name"], boss["hp"])
        else:
            #boss turn
            #update the player hp
            hero["hp"] = int(hero["hp"]) - int(boss_attack())
            show_turn_info(hero["name"], hero["hp"])
        turn += 1
    
def show_turn_info(victim, hp):
    print("-------------------------------------------")
    if int(hp) <= 0: #out of hp
        print(victim, "has been defeated")
        input("Thank you for playing :')")
        exit()
    else:
        print(victim, "has gone down to ", hp, " hp")
    print("-------------------------------------------")

  
#main flow
get_hero_data()
get_event_data()
show_menu()
roll_the_dice()
