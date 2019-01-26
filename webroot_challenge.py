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

current_move = 0
current_index = 0
patrol_points = [('4000', '2000'), ('8000', '2000'), ('12000', '2000'), \
                 ('10000', '6000'), ('6000', '6000'), ('2000', '6000')]

# patrol_points = [(i, j) for i in range(2000, x, 2000) for j in range(2000, y, 2000)]

def distance(player, ghost):
    return math.sqrt(((player[1] - ghost[1]) ** 2) + ((player[0] - ghost[0]) ** 2))


def assign_values(coords, state, value):
    return {'coords': coords, 'state': state, 'value': value}
    
    
def assign_closest(player, ghosts):
    
    def distance(ghost):
        return math.sqrt(((player[1] - ghost['coords'][1]) ** 2) + \
                         ((player[0] - ghost['coords'][0]) ** 2))
    
    if len(ghosts):
        ghosts.sort(key=distance)
        return ghosts[0]
    else:
        return None
        
def best_direction(ghost):
    x = ghost[0]
    y = ghost[1]
    
    if x - 500 > 0:
        return (x - 500, y)
    elif y - 500 > 0:
        return (x, y - 500)
    elif x + 500 < 16000:
        return (x + 500, y)
    else:
        return (x, y + 500)
    

# game loop
while True:
    entities = int(input())  # the number of busters and ghosts visible to you
    
    data = ['coords', 'state', 'value']
    ghosts = []
    
    hunter = {i: () for i in data}
    catcher = {i: () for i in data}
    support = {i: () for i in data}
    
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
                hunter = assign_values((x, y), state, value)
            elif entity_role == 1:
                catcher = assign_values((x, y), state, value)
            elif entity_role == 2:
                support = assign_values((x, y), state, value)
      
    closest_ghost =  assign_closest(hunter['coords'], ghosts)
    
    # IDENTIFY CLOSEST TARGET #
    if closest_ghost:
        closest_x = str(closest_ghost['coords'][0])
        closest_y = str(closest_ghost['coords'][1])
    else:
        closest_x = "8000"
        closest_y = "4500"
    
    # HUNTER MOVEMENT #
    if closest_ghost:
        dist_ghost = distance(hunter['coords'], closest_ghost['coords'])
        if dist_ghost < 1760 and dist_ghost > 900 and closest_ghost['stamina']:
            busting = True
            print("BUST " + str(closest_ghost['id']))
        elif dist_ghost < 900:
            move_coords = best_direction(closest_ghost['coords'])
            print("MOVE " + str(move_coords[0]) + " " + str(move_coords[1]))
        else:
            print("MOVE " + closest_x + " " + closest_y)
    else:
        print("MOVE " + patrol_points[current_index][0] + " " + patrol_points[current_index][1])
    
    # CATCHER MOVEMENT #
    if catcher['state'] == 1:
        catcher_x = catcher['coords'][0]
        catcher_y = catcher['coords'][1]
        if my_team_id == 0:
            if catcher_x <= 900 and catcher_y <= 900:
                print("RELEASE")
            else:
                print("MOVE 900 900")
        else:
            if catcher_x == 15100 and catcher_y == 15100:
                print("RELEASE")
            else:
                print("MOVE 15100 15100")
    elif closest_ghost:
        dist_ghost = distance(catcher['coords'], closest_ghost['coords'])
        
        # closest_to_catcher =  assign_closest(catcher['coords'], ghosts)
        
        if dist_ghost > 1000:
            print("MOVE " + closest_x + " " + closest_y)
        
        elif not closest_ghost['stamina'] and not catcher['state'] and \
                 ((closest_ghost['coords'][0] > 1200 and closest_ghost['coords'][1] > 1200) and \
                  (closest_ghost['coords'][0] < 14800 and closest_ghost['coords'][1] < 14800)):
            print("TRAP " + str(closest_ghost['id']))
            
        elif dist_ghost < 900:
            move_coords = best_direction(closest_ghost['coords'])
            print("MOVE " + str(move_coords[0]) + " " + str(move_coords[1]))
            
        
            
        else:
            print("MOVE " + closest_x + " " + closest_y)
    else:
        print("MOVE " + patrol_points[current_index][0] + " " + patrol_points[current_index][1])
        
        
    # SUPPORT MOVEMENT #
    print("MOVE " + patrol_points[current_index][0] + " " + patrol_points[current_index][1])
    
    
    current_move += 1
    
    if current_move % 6 == 0:
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