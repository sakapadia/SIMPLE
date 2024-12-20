import random
# carparts = blue = 0,  maroon = 1, green = 2, pink = 3, beige = 4, grey = 5
class Player():
    def __init__(self, id):
        self.id = id
        self.workstation_id = 0 # set to whereever the meeple is
        self.points = 0
        self.actions = 0
        self.position = Position()
        self.books = 0
        self.wildParts = 0
        self.speechBubbles = 1
        self.bankShifts = 0
        self.wildPartsGained = 0
        self.speechBubblesGained = 0
        self.booksGained = 0
        self.designTiles = []
        self.parts = []
        self.kanbanOrders = [] #can be a tuple too
        self.garages = [] #self.garage = Garage()
        numbers = list(range(4))
        # Shuffle the list in place
        random.shuffle(numbers)
        garageRewards = numbers
        # Create a new Garage instance and append it to the garages list
        garage1 = Garage(0, 1, garageRewards[0], None, self)
        garage2 = Garage(0, 1, garageRewards[1], None, self)
        garage3 = Garage(0, 1, garageRewards[2], None, self)
        garage4 = Garage(0, 1, garageRewards[3], None, self)
        garage5 = Garage(0, 1, 4, None, self)
        self.garages.append(garage1)
        self.garages.append(garage2)
        self.garages.append(garage3)
        self.garages.append(garage4)
        self.garages.append(garage5)
        self.designs = [] #5 Design Tiles where 1 is locked
        self.certifications = [] # 5 booleans

class Garage():
    def __init__(self, id, order, reward, car, player):
        self.id = id
        self.order = order # numbers 1-5
        self.rewardID = reward # reward 1-5 associated w/ garage
        self.car = car
        self.player = player

    def addCar(self, car):
        self.car = car
        if self.rewardID == 0:
            self.player.booksGained += 2
        elif self.rewardID == 1:
            self.player.wildPartsGained += 2
        elif self.rewardID == 2:
            self.player.speechBubblesGained += 1
        elif self.rewardID == 3:
            self.player.bankShifts += 2
        elif self.rewardID == 4:
            #certified
            if self.player.certified[0]:
                # TODO pick 1/4 do something 
                self.player.wildPartsGained += 1
                self.player.speechBubblesGained += 1
                self.player.bankShifts += 1
                self.player.booksGained += 1
            pass

class Tile():
    def __init__(self, id, order, name):
        self.id = id
        self.order = order
        self.name = name

class KanbanOrder(Tile):
    def __init__(self, id, order, name, parts):
        self.id = id
        self.order = order # numbers 1-5
        self.name = name
        self.parts = parts

class Butterfly(Tile):
    def __init__(self, id, order, name, colour, value):
        super(Butterfly, self).__init__(id, order, name)
        self.colour = colour
        self.value = value
        self.type = f'{colour}butterfly'
        if colour == 'G':
            colour_icon = '🟢'
        elif colour == 'B':
            colour_icon = '🔵'
        elif colour == 'Y':
            colour_icon = '🟡'
        elif colour == 'R':
            colour_icon = '🔴'
            
        self.symbol = f'{colour_icon}{value}' if value > 0 else f'{colour_icon}X'

class Flower(Tile):
    def __init__(self, id, order, name):
        super(Flower, self).__init__(id, order, name)
        self.type = 'flower'
        self.symbol = '🌼'

class Car(Tile):
    def __init__(self, id, order, name, color):
        super(Car, self).__init__(id, order, name)
        self.color = color
        if color == 'green':
            self.value = 2
        elif color == 'blue':
            self.value = 3
        elif color == 'grey':
            self.value = 4
        elif color == 'red':
            self.value = 5
        elif color == 'black':
            self.value = 6
        self.symbol = '🌼'
        self.upgrades = []

    #def availableUpgrades(self)

    def upgrade(self, partID):
        if partID in self.upgrades:
            return False
        self.upgrades.append(partID)
        return True


class Bee(Tile):
    def __init__(self, id, order, name):
        super(Bee, self).__init__(id, order, name)
        self.type = 'bee'
        self.value = -3
        self.symbol = 'BEE'


class DrawBag():
    def __init__(self, contents):
        self.contents = contents
        self.create()
    
    def shuffle(self):
        random.shuffle(self.tiles)

    def draw(self, n):
        drawn = []
        for x in range(n):
            drawn.append(self.tiles.pop())
        return drawn
    
    def add(self, tiles):
        for tile in tiles:
            self.tiles.append(tile)

    def create(self):
        self.tiles = []

        tile_id = 0
        for order, x in enumerate(self.contents):
            x['info']['order'] = order
            for i in range(x['count']):
                x['info']['id'] = tile_id
                self.add([x['tile'](**x['info'])])
                tile_id += 1
                
        self.shuffle()
                
    def size(self):
        return len(self.tiles)


class Position():
    def __init__(self):
        self.tiles = []  
    
    def add(self, tiles):
        for tile in tiles:
            self.tiles.append(tile)
    
    def size(self):
        return len(self.tiles)

    @property
    def score(self):
        score = 0
        #BUTTERFLIES
        for colour in ['R','B','G','Y']:
            tile_values = [t.value for t in self.tiles if t.type == f'{colour}butterfly']
            s = sum(tile_values)
            if 0 in tile_values:
                s *= 2
            
            score += s
        
        #FLOWERS
        count = len([t for t in self.tiles if t.type == f'flower'])
        score += pow(count, 2)

        #DRAGONFLY
        drag = [t.value for t in self.tiles if t.type == f'dragonfly']
        if len(drag) > 0:
            score += max(drag)

        #LIGHTNINGBUG
        lb = [t.value for t in self.tiles if t.type == f'lightningbug']
        if len(lb) > 0:
            score += min(lb)

        #CRICKET
        cricket = [t.value for t in self.tiles if t.type == f'cricket']
        if len(cricket) > 0:
            score += cricket[-1]

        #BEE / HONEYCOMB
        bees = [t.value for t in self.tiles if t.type == f'bee']
        honeycomb = sorted([t.value for t in self.tiles if t.type == f'honeycomb'], reverse = True)

        score += sum(honeycomb[:len(bees)])
        score += sum(bees[len(honeycomb):])

        #WASP
        score += sum([t.value for t in self.tiles if t.type == f'wasp'])

        return score
        
class DesignDepartment:
    def __init__(self):
        self.designs = []  # List of available designs (populate during setup)
        self.workstations = []  # Status of workstations (occupied = True)

    def select_design(self, player, design_index):
        # Logic for selecting a design
        # player: The player object
        # design_index: The index of the chosen design in self.designs
        if self.workstations[player.workstation_id]: # Check if workstation is occupied
            chosen_design = self.designs.pop(design_index)
            player.designs.append(chosen_design)
            # Apply any design selection bonuses (Banked Shifts, Books, etc.)
            if design_index < 2:
                player.booksGained += 1
            elif design_index < 4:
                player.bankShifts += 1
        else:
            # Handle case where workstation is not occupied (e.g., penalty)
            pass

    #Determines the legal actions a player can take in the Design Department.
    def get_legal_actions(self, player): 
        # player: The player object
        # Returns:  A list representing legal action IDs (e.g., 0 for select_design) 
        legal_actions = []
        if self.workstations[player.workstation_id]: 
            if player.can_select_design(): # Check player-specific conditions
                legal_actions.append(0)  # 0 represents "select_design" action
        return legal_actions
    
    def populateDesigns(self):
        #use drawbag to add 10 random Design tiles where 0-1 give books and 2-3 give shifts 8-9 are locked
        pass
    


class LogisticsDepartment:
    def __init__(self):
        self.warehouses = {} # Dictionary to store car parts in warehouses
        self.kanban_deck = [] # Deck of Kanban cards (populate during setup)
        self.workstations = [False, False] # Status of workstations 

    def issue_kanban_order(self, player, card_index):
        #Player issues a Kanban order to stock warehouses.
        #player: The player object
        #card_index: The index of the Kanban card in the player's hand
        if self.workstations[player.workstation_id]:
            if player.can_issue_kanban_order(): 
                kanban_card = player.hand.pop(card_index)
                # Implement Kanban card logic to replenish warehouses 
                player.hand.append(self.kanban_deck.pop()) # Draw new card
                # Apply any Kanban order bonuses (e.g., Banked Shift)
        else:
            # Handle unoccupied workstation
            pass

    # Player collects car parts from a warehouse.
    def collect_car_parts(self, player, warehouse_id, quantity):
        #player: The player object
        # warehouse_id: ID of the warehouse to collect from
        # quantity: Number of parts to collect 
        if self.workstations[player.workstation_id]:
            if player.can_collect_car_parts():
                # Implement logic to transfer parts from warehouse to player 
                # (Check availability, storage limits, etc.)
                pass
        else: 
            # Handle unoccupied workstation
            pass

    def get_legal_actions(self, player):
        legal_actions = []
        if self.workstations[player.workstation_id]:
            if player.can_issue_kanban_order():
                legal_actions.append(0) # Issue Kanban order
            if player.can_collect_car_parts(): 
                legal_actions.append(1) # Collect car parts
        return legal_actions

class AssemblyDepartment:
    def __init__(self):
        self.assembly_lines = {} # Data structure to represent assembly lines
        self.demand_tiles = [] # Current demand tiles (populate during setup)
        self.workstations = [False, False]

    def provide_needed_part(self, player, part_type, assembly_line_id):
        # Player provides a car part to an assembly line.
            #player: The player object
            #part_type: The type of car part being provided
            #assembly_line_id: The ID of the target assembly line
        if self.workstations[player.workstation_id]:
            if player.can_provide_part():
                # Implement logic to:
                #  - Check if the part type is valid for the assembly line
                #  - Deduct the part from the player or use a Parts Voucher
                #  - Advance cars on the assembly line (potentially triggering scoring)
                #  - Replenish the assembly line with a new car if needed 
                #  - Award Speech tokens for fulfilling demand
                pass
        else:
            # Handle unoccupied workstation
            pass 

    def get_legal_actions(self, player):
        legal_actions = [] 
        if self.workstations[player.workstation_id]: 
            if player.can_provide_part():
                legal_actions.append(0) # Provide car part
        return legal_actions
    
class ResearchDepartment():
    def __init__(self):
        self.workstations = [None, None]
        track = {}
        self.greenCar = Car()
        self.blueCar = Car()
        self.greyCar = Car()
        self.redCar = Car()
        self.blackCar = Car()
        # arrays of 6, index represents reward value
        self.greenRewards = []
        self.blueRewards = []
        self.greyRewards = []
        self.redRewards = []
        self.blackRewards = []
    
    def upgrade_car(self, carColor, partId, rewardIndex, player):
        answer = False
        if carColor == 'green':
            answer = self.greenCar.upgrade(partId)
        elif carColor == 'blue':
            answer = self.blueCar.upgrade(partId)
        elif carColor == 'grey':
            answer = self.greyCar.upgrade(partId)
        elif carColor == 'red':
            answer = self.redCar.upgrade(partId)
        elif carColor == 'black':
            answer = self.blackCar.upgrade(partId)
            self.pickReward(self.blackCar, rewardIndex, player)
        player.points += 2
        return answer
    
    def pickReward(self, car, index, player):
        if car.color == 'green':
            if index in self.greenRewards:
                return False
            if index == 1 or index == 2:
                player.bankShifts += 1
            elif index == 3:
                player.points += 4
            elif index == 4:
                player.points += 3
            self.greenRewards.append(index)
            return True
        elif car.color == 'blue':
            if index in self.blueRewards:
                return False
            if index == 1:
                player.bankShifts += 1
            elif index == 3:
                player.points += 3
            elif index == 4:
                player.points += 2
            self.blueRewards.append(index)
        elif car.color == 'grey':
            if index in self.greyRewards:
                return False
            if index == 1:
                player.bankShifts += 1
            elif index == 3:
                player.points += 2
            self.greyRewards.append(index)
        elif car.color == 'red':
            if index in self.redRewards:
                return False
            elif index == 3:
                player.points += 1
            self.redRewards.append(index)
        elif car.color == 'black':
            if index in self.blackRewards:
                return False
            self.blackRewards.append(index)
        # these rewards are common to all cars
        if index == 0:
            player.bankShifts += 1
        elif index == 5:
            player.booksGained += 1
        return True
    
    def claim_cars(self, player, car_indices):
        #Player claims cars from the test track.
        #player: The player object
        #car_indices: A list of indices of cars to claim
        if self.workstations[player.workstation_id]:
            if player.can_claim_cars():
                # Implement logic to:
                #   - Verify the player has matching designs for the cars
                #   - Deduct designs and spend Shifts based on car positions
                #   - Transfer cars from test track to player's garage
                #   - Advance the Pace Car and trigger Meetings if needed
                #   - Apply garage bonuses
                pass 
        else: 
            # Handle unoccupied workstation
            pass

    def train(self):
        pass
    
    def get_legal_actions(self, player):
        legal_actions = []
        if self.workstations[player.workstation_id]:
            if player.can_claim_cars():
                legal_actions.append(0) # Claim cars
            if player.can_upgrade_design():
                legal_actions.append(1) # Upgrade design
        return legal_actions

class AdministrationDepartment: 
    def __init__(self):
        self.workstations = [False] # Only one workstation 

    def train(self, player):
        # Player trains in Administration, allowing them to choose another department.
            # player: The player object
        if self.workstations[player.workstation_id]:
            # Implement training logic, allowing player to choose another department
            # for additional actions. 
            pass
        else:
            # Handle unoccupied workstation
            pass

    def get_legal_actions(self, player):
        legal_actions = []
        if self.workstations[player.workstation_id]:
            legal_actions.append(0) # Train in Administration
        return legal_actions

class Board():
    def __init__(self, size):
        self.size = size
        self.squares = size * size
        self.tiles = [None] * self.squares 
        self.nets = [False] * self.squares 
        self.hudson = 0
        self.hudson_facing = 'R'
    
    def add_net(self, position):
        self.nets[position] = True
    
    def remove(self, position):
        tile = self.tiles[position]
        self.tiles[position] = None
        return tile

    def fill(self, tiles):
        self.tiles = tiles