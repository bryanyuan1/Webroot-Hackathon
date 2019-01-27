import sys
import math
import random

# Send your busters out into the fog to trap ghosts and bring them home!

busters_per_player = int(input())  # the amount of busters you control
ghost_count = int(input())  # the amount of ghosts on the map
my_team_id = int(input())  # if this is 0, your base is on the top left of the map, if it is one, on the bottom right

x = 16000
y = 9000

move_from_ghost = 0

stunned = 0

ghost_id = None

if my_team_id == 1:
    last_known_location = (1500, 1500)
else:
    last_known_location = (14500, 7500)

found_catcher = False
dropped_ghost = False

current_move = 0
current_index = 0
patrol_points = [('5000', '1900'), ('10000', '1900'), ('15000', '1900'), \
                 ('10000', '7000'), ('6000', '7000'), ('2200', '7000')]

# patrol_points = [(i, j) for i in range(2000, x, 2000) for j in range(2000, y, 2000)]

def distance(player, ghost):
    return math.sqrt(((player[1] - ghost[1]) ** 2) + ((player[0] - ghost[0]) ** 2))


def assign_values(coords, state, value, entity_id):
    return {'coords': coords, 'state': state, 'value': value, 'id': entity_id}
    
    
def assign_closest(player, ghosts):
    
    def distance(ghost):
        return math.sqrt(((player[1] - ghost['coords'][1]) ** 2) + \
                         ((player[0] - ghost['coords'][0]) ** 2))
    
    if len(ghosts):
        ghosts.sort(key=distance)
        return ghosts[0]
    else:
        return None
        

def assign_catcher(ghosts):
    
    if len(ghosts):
        ghosts.sort(key=lambda x: x['stamina'])
        return ghosts[0]
    else:
        return None

        
def best_direction(ghost):
    x = ghost[0]
    y = ghost[1]
    
    if x - 900 > 0:
        return (x - 900, y)
    elif y - 900 > 0:
        return (x, y - 900)
    elif x + 900 < 16000:
        return (x + 900, y)
    else:
        return (x, y + 900)
        

# game loop
while True:
    entities = int(input())  # the number of busters and ghosts visible to you
    
    data = ['coords', 'state', 'value', 'id']
    ghosts = []
    
    hunter = {i: () for i in data}
    catcher = {i: () for i in data}
    support = {i: () for i in data}
    
    oppo_hunter = {i: () for i in data}
    oppo_catcher = {i: () for i in data}
    oppo_support = {i: () for i in data}
    
    
    busting = False
    
    for i in range(entities):
        # entity_id: buster id or ghost id
        # y: position of this buster / ghost
        # entity_type: the team id if it is a buster, -1 if it is a ghost.
        # entity_role: -1 for ghosts, 0 for the HUNTER, 1 for the GHOST CATCHER and 2 for the SUPPORT
        # state: For busters: 0=idle, 1=carrying a ghost. For ghosts: remaining stamina points.
        # value: For busters: Ghost id being carried/busted or number of turns left when stunned. For ghosts: number of busters attempting to trap this ghost.
        entity_id, x, y, entity_type, entity_role, state, value = [int(j) for j in input().split()]
        
        if entity_role == -1:
            ghosts.append({'coords': (x,y), 'id': entity_id, 'stamina': state})
            # ghosts.append((x, y))
        elif entity_type == my_team_id:
            if entity_role == 0:
                hunter = assign_values((x, y), state, value, entity_id)
            elif entity_role == 1:
                catcher = assign_values((x, y), state, value, entity_id)
            elif entity_role == 2:
                support = assign_values((x, y), state, value, entity_id)
        else:
            if entity_role == 0:
                oppo_hunter = assign_values((x, y), state, value, entity_id)
            elif entity_role == 1:
                oppo_catcher = assign_values((x, y), state, value, entity_id)
            elif entity_role == 2:
                oppo_support = assign_values((x, y), state, value, entity_id)
      
    closest_ghost =  assign_closest(hunter['coords'], ghosts)
    
    # IDENTIFY CLOSEST TARGET #
    if closest_ghost:
        closest_x = str(closest_ghost['coords'][0])
        closest_y = str(closest_ghost['coords'][1])
        
    # we may not use the center because we already got the patrol
    #else:
        #closest_x = "8000"
        #closest_y = "4500"
    
    # HUNTER MOVEMENT #
    if closest_ghost:
        dist_ghost = distance(hunter['coords'], closest_ghost['coords'])
        if dist_ghost < 1760 and dist_ghost > 900 and closest_ghost['stamina']:
            busting = True
            print("BUST " + str(closest_ghost['id']))
        elif dist_ghost < 900:
            #move_coords = best_direction(closest_ghost['coords'])
            print("MOVE " + str(hunter['coords'][0]) + " " + str(hunter['coords'][1]))
        else:
            print("MOVE " + closest_x + " " + closest_y)
    else:
        print("MOVE " + patrol_points[current_index][0] + " " + patrol_points[current_index][1])
    
    
    """ LOOKS FOR CLOSEST GHOST
    
    # CATCHER MOVEMENT #
    if catcher['state'] == 1:
        catcher_x = catcher['coords'][0]
        catcher_y = catcher['coords'][1]
        if my_team_id == 0:
            if catcher_x <= 900 and catcher_y <= 900:
                print("RELEASE")
            else:
                print("MOVE 500 500")
        else:
            if catcher_x >= 15100 and catcher_y >= 8100:
                print("RELEASE")
            else:
                print("MOVE 15500 8500")
    
    #not carrying and find a ghost
    elif closest_ghost:
        # if the hunter is still firing, i will go to hunter; if the hunter finishes firing
        # i will go there and carry! Also, the ghost should not be in the base!
        dist_ghost = distance(catcher['coords'], closest_ghost['coords'])
        
        # closest_to_catcher =  assign_closest(catcher['coords'], ghosts)
        
        #hunter is firing
        if closest_ghost['stamina'] > 0:
            print("MOVE " + str(hunter['coords'][0]) + " " + str(hunter['coords'][1]))
        
        # hunter finishes
        else: 
            if dist_ghost > 1600:
                print("MOVE " + closest_x + " " + closest_y)
                
            elif dist_ghost < 900:
                #move_coords = best_direction(closest_ghost['coords'])
                #just stop and the ghost runs for you
                print("MOVE " + str(catcher['coords'][0]) + " " + str(catcher['coords'][1]))
                
            #this is when it is in catch range, and not in base
            elif (not(closest_ghost['coords'][0] < 1200 and closest_ghost['coords'][1] < 1200) and \
                      not(closest_ghost['coords'][0] > 14800 and closest_ghost['coords'][1] > 7800)):
                print("TRAP " + str(closest_ghost['id']))
    
    else:
        print("MOVE " + str(hunter['coords'][0]) + " " + str(hunter['coords'][1]))
    """    
    
    # CATCHER MOVEMENT # LOOKS FOR WEAKEST GHOST
    """
    catcher_closest = assign_catcher(ghosts)
    
    if catcher['state'] == 1:
        catcher_x = catcher['coords'][0]
        catcher_y = catcher['coords'][1]
        if my_team_id == 0:
            if catcher_x <= 900 and catcher_y <= 900:
                print("RELEASE")
            else:
                print("MOVE 500 500")
        else:
            if catcher_x >= 15100 and catcher_y >= 8100:
                print("RELEASE")
            else:
                print("MOVE 15500 8500")
    
    #not carrying and find a ghost
    elif catcher_closest:
        # if the hunter is still firing, i will go to hunter; if the hunter finishes firing
        # i will go there and carry! Also, the ghost should not be in the base!
        dist_ghost = distance(catcher['coords'], catcher_closest['coords'])
        
        # closest_to_catcher =  assign_closest(catcher['coords'], ghosts)
        
        #hunter is firing
        if catcher_closest['stamina'] > 0:
            print("MOVE " + str(hunter['coords'][0]) + " " + str(hunter['coords'][1]))
        
        # hunter finishes
        else: 
            if dist_ghost > 1600:
                print("MOVE " + closest_x + " " + closest_y)
                
            elif dist_ghost < 900:
                #move_coords = best_direction(closest_ghost['coords'])
                #just stop and the ghost runs for you
                print("MOVE " + str(catcher['coords'][0]) + " " + str(catcher['coords'][1]))
                
            #this is when it is in catch range, and not in base
            elif (not(catcher_closest['coords'][0] < 1200 and catcher_closest['coords'][1] < 1200) and \
                      not(catcher_closest['coords'][0] > 14800 and catcher_closest['coords'][1] > 7800)):
                print("TRAP " + str(catcher_closest['id']))
    
    else:
        print("MOVE " + str(hunter['coords'][0]) + " " + str(hunter['coords'][1]))
    """
    
    
    # CATCHER FOLLOW CATCHER
    closest_to_support = assign_closest(support['coords'], ghosts)
    lowest_stamina = assign_catcher(ghosts)
    
    if catcher['state'] == 1:
        catcher_x = catcher['coords'][0]
        catcher_y = catcher['coords'][1]
        if my_team_id == 0:
            if catcher_x <= 900 and catcher_y <= 900:
                print("RELEASE")
            else:
                print("MOVE 500 500")
        else:
            if catcher_x >= 15100 and catcher_y >= 8100:
                print("RELEASE")
            else:
                print("MOVE 15500 8500")
    
    #not carrying and find a ghost
    elif closest_ghost != None and closest_ghost['stamina'] == 0:
        dist_to_cg = distance(catcher['coords'], closest_ghost['coords'])
        best_choice = best_direction(closest_ghost['coords'])
        
        if dist_to_cg > 1760:
            print("MOVE " + str(best_choice[0]) + " " + str(best_choice[1]))
            
        elif dist_to_cg < 900:
            print("MOVE " + str(best_choice[0]) + " " + str(best_choice[1]))
        
        else:
            print("TRAP " + str(closest_ghost['id']))
        
        
    elif lowest_stamina != None and lowest_stamina['stamina'] == 0:
        dist_to_ls = distance(catcher['coords'], lowest_stamina['coords'])
        best_choice = best_direction(lowest_stamina['coords'])
        
        if dist_to_ls > 1760:
            print("MOVE " + str(best_choice[0]) + " " + str(best_choice[1]))
            
        elif dist_to_ls < 900:
            print("MOVE " + str(best_choice[0]) + " " + str(best_choice[1]))
        
        else:
            print("TRAP " + str(lowest_stamina['id']))
        
        
    elif closest_to_support:
        dist_to_cts = distance(catcher['coords'], closest_to_support['coords'])
        best_choice = best_direction(closest_to_support['coords'])
        # hunter finishes
        if dist_to_cts > 1760:
            print("MOVE " + str(best_choice[0]) + " " + str(best_choice[1]))
            
        elif dist_to_cts < 900:
            #move_coords = best_direction(closest_ghost['coords'])
            #just stop and the ghost runs for you
            print("MOVE " + str(best_choice[0]) + " " + str(best_choice[1]))
            
        #this is when it is in catch range, and not in base
        elif (not(closest_to_support['coords'][0] < 1200 and closest_to_support['coords'][1] < 1200) and \
                  not(closest_to_support['coords'][0] > 14800 and closest_to_support['coords'][1] > 7800)):
            print("TRAP " + str(closest_to_support['id']))
        else:
            print("MOVE " + str(catcher['coords'][0]) + " " + str(catcher['coords'][0]))
    
    else:
        print("MOVE " + str(support['coords'][0]) + " " + str(support['coords'][1]))
    
    
    # SUPPORT MOVEMENT #
    
    """
    if oppo_catcher['id'] != ():
        if not found_catcher:
            found_catcher = True
        if distance(support['coords'], oppo_catcher['coords']) < 1760:
            if oppo_catcher['state'] == 1:
                ghost_id = oppo_catcher['value']
                dropped_ghost = True
            else:
                dropped_ghost = False
            print("STUN " + str(oppo_catcher['id']))
        else:
            print("MOVE " + str(oppo_catcher['coords'][0]) + " " + str(oppo_catcher['coords'][1]))
    elif not found_catcher:
        if my_team_id == 1:
            print("MOVE 1500 1500")
        else:
            print("MOVE 14500 7500")
    else:
        if my_team_id == 1:
            print("MOVE 1500 1500")
        else:
            print("MOVE 14500 7500")
    """
            
    # SUPPORT FOLLOW CATCHER
    if current_move == 10:
        print("RADAR")
    elif oppo_catcher['id'] != ():
        last_known_location = oppo_catcher['coords']
        if not found_catcher:
            found_catcher = True
        if distance(support['coords'], oppo_catcher['coords']) < 1760 and oppo_catcher['state'] == 1 and \
            stunned == 0: #stunned <= 0:
            stunned = 21
            print("STUN " + str(oppo_catcher['id']))
        else:
            print("MOVE " + str(oppo_catcher['coords'][0]) + " " + str(oppo_catcher['coords'][1]))
    elif not found_catcher:
        print("MOVE " + str(last_known_location[0]) + " " + str(last_known_location[1])) 
    else:
        print("MOVE " + str(last_known_location[0]) + " " + str(last_known_location[1])) 
    
    if stunned > 0:
        stunned -= 1
    
    # SUPPORT FOLLOW HUNTER
    """
    if current_move == 10:
        print("RADAR")
    elif oppo_hunter['id'] != ():
        last_known_location = oppo_hunter['coords']
        if not found_catcher:
            found_catcher = True
        if distance(support['coords'], oppo_hunter['coords']) < 1760 and stunned <= 0:
            stunned = 10
            print("STUN " + str(oppo_hunter['id']))
        else:
            stunned -= 1
            print("MOVE " + str(oppo_hunter['coords'][0]) + " " + str(oppo_hunter['coords'][1]))
    elif not found_catcher:
        print("MOVE " + str(last_known_location[0]) + " " + str(last_known_location[1])) 
    else:
        print("MOVE " + str(last_known_location[0]) + " " + str(last_known_location[1])) 
    """
    
    
    current_move += 1
    
    if current_move % 8 == 0:
        current_index = (current_index + 1) % 6
    
    # print(current_move, file=sys.stderr)
        

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)


    # First the HUNTER : MOVE x y | BUST id
    # Second the GHOST CATCHER: MOVE x y | TRAP id | RELEASE
    # Third the SUPPORT: MOVE x y | STUN id | RADAR
    
    # print("MOVE 8000 4500")
    # print("MOVE 8000 4500")
    # print("MOVE 8000 4500")