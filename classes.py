import numpy as np

# Class defining a person
class person:
    # Constructor method
    def __init__(self, id, environment_dim, places, trans_matrix, type, inf_status):
        # Define the id
        self.id = id
        # Define the home position at random, at beginning coincide with actual position
        self.position = [0, 0]
        self.position[0] = np.random.randint(0, environment_dim[0]) # X aka columns
        self.position[1] = np.random.randint(0, environment_dim[1]) # Y aka rows
        # Define goal
        self.goal = 0
        # Define places: home is always the first places[0]
        self.places = [self.position] + places
        # Define transition matrix
        self.trans_matrix = trans_matrix
        # Define type
        self.type = type
        # Define infection status
        self.inf_status = inf_status # 0: healty, >0: infected, >=infection_duration: immune
        # Define first next goal
        self.next_goal()

    # Movement method
    def move(self):
        origin = self.position
        destination = self.places[self.goal]
        if np.array_equal(origin, destination): # Destination already reached
            self.next_goal()
            destination = self.places[self.goal]
        deltaX = destination[0] - origin[0]
        deltaY = destination[1] - origin[1]
        delta = abs(deltaX) + abs(deltaY)
        if delta > 0:
            direction = rand_from_list([abs(deltaX)/delta, abs(deltaY)/delta])
            if direction == 0:
                self.position[0] += np.sign(deltaX) # Lateral movement
            else:
                self.position[1] += np.sign(deltaY) # Vertical movement

    # Compute next goal method
    def next_goal(self):
        self.goal = rand_from_list(self.trans_matrix[self.goal][:])

    # Representation method
    def __repr__(self):
        return 'ID: '+str(self.id)+' PosX: '+str(self.position[0])+' PosY: '+str(self.position[1])+' GoalX: '+str(self.places[self.goal][0])+' GoalY: '+str(self.places[self.goal][1])

# Function computing random integer according to a distribution as list
def rand_from_list(p):
    if abs(1. - sum(p)) > 1e-6:
        new_p = []
        for i in range(len(p)):
            new_p.append(round(p[i], 2))
        p = new_p
    N = len(p)
    x = np.random.random()
    s = 0
    for n in range(N):
        s += p[n]
        if x < s:
            return n
